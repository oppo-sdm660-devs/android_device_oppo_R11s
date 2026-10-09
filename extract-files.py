#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from hashlib import sha256
from pathlib import Path

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/oppo/R11s',
    'device/oppo/sdm660-common',
    'hardware/qcom-caf/sdm660',
    'vendor/oppo/sdm660-common'
]


def fixup_s5k2p7sq_pipeline_delay(_ctx, _file, file_path, **_kwargs):
    path = Path(file_path)
    data = path.read_bytes()
    original = 'f364f5611addb4b7e84e90c5adaa212b3a3d704af87b3b652619a407724ad21b'
    fixed = '02953b1b2f49a04ac9fb199efc8183ad516717452149cb913847cd944e8e6096'
    digest = sha256(data).hexdigest()
    if digest == fixed:
        return
    # sensor_lib_t +0x260: command application and metadata must use delay=2.
    if digest != original or data[0x4268:0x426c] != bytes.fromhex('01000000'):
        raise ValueError('Unrecognized s5k2p7sq pipeline-delay layout')
    data = data[:0x4268] + bytes.fromhex('02000000') + data[0x426c:]
    if sha256(data).hexdigest() != fixed:
        raise ValueError('s5k2p7sq pipeline-delay output differs from the verified library')
    path.write_bytes(data)


blob_fixups: blob_fixups_user_type = {
    'vendor/lib/libmmcamera_s5k2p7sq.so': blob_fixup()
        .call(fixup_s5k2p7sq_pipeline_delay, need_tmp_dir=False),
    # Stock 3A uses the HIDL transport symbols now provided by libhidlbase.
    'vendor/lib/libmmcamera2_stats_modules.so': blob_fixup()
        .remove_needed('libhidltransport.so'),
    'vendor/bin/qfp-daemon': blob_fixup()
        .replace_needed('libhidltransport.so', 'libhidlbase.so'),
    (
        'vendor/lib64/android.frameworks.fingerprintservice@1.0.so',
        'vendor/lib64/vendor.oppo.hardware.commondcs@1.0.so',
        'vendor/lib64/vendor.qti.hardware.fingerprint@1.0.so'
    ): blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'R11s',
    'oppo',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sdm660-common', module.vendor)
    utils.run()
