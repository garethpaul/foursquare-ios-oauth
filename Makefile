PROJECT := FSExampleOAuth/FSExampleOAuth.xcodeproj
SCHEME := FSExampleOAuth
DERIVED_DATA ?= $(CURDIR)/.derived-data
XCODE_FLAGS := \
	-project "$(PROJECT)" \
	-scheme "$(SCHEME)" \
	-configuration Debug \
	-sdk iphonesimulator \
	-destination "generic/platform=iOS Simulator" \
	-derivedDataPath "$(DERIVED_DATA)" \
	IPHONEOS_DEPLOYMENT_TARGET=12.0 \
	PRODUCT_BUNDLE_IDENTIFIER=com.foursquare.FSExampleOAuth \
	CODE_SIGNING_ALLOWED=NO \
	CODE_SIGNING_REQUIRED=NO \
	CODE_SIGN_IDENTITY=

.PHONY: check test analyze build clean

check: test analyze build

test:
	python3 -m unittest discover -s tests -v

analyze:
	xcodebuild analyze $(XCODE_FLAGS)

build:
	xcodebuild build $(XCODE_FLAGS)

clean:
	rm -rf "$(DERIVED_DATA)"
