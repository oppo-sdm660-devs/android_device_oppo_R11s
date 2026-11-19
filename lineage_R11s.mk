#
# Copyright (C) 2025 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit some common Lineage stuff.
PRODUCT_NO_CAMERA := true
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit from R11s device
$(call inherit-product, device/oppo/R11s/device.mk)

PRODUCT_DEVICE := R11s
PRODUCT_NAME := lineage_R11s
PRODUCT_BRAND := OPPO
PRODUCT_MODEL := OPPO R11s
PRODUCT_MANUFACTURER := OPPO

PRODUCT_GMS_CLIENTID_BASE := android-oppo

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="sdm660_64-user 9 PKQ1.190414.001 eng.root.20200522.190302 release-keys" \
    BuildFingerprint=OPPO/R11s/R11s:9/PKQ1.190414.001/1588166940:user/release-keys
