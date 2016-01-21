#!/bin/bash
# Rename a fucking Xcode project since Xcode is a steaming pile.
# Copyright © 2015 WalmartLabs. All rights reserved.

# run this command before running this script:
#   brew install rename ack

# Usage: xcoderename.sh OldName NewName
# This will rename OldName to NewName in all filenames and their contents.

git mv "$1" "$2"
git mv "$1Tests" "$2Tests"
git mv "$1.xcodeproj" "$2.xcodeproj"

# may need to run this a few times.
find . -name "$1*" -print0 | xargs -0 rename -S "$1" "$2"
ack --literal --files-with-matches "$1" | xargs sed -i "" "s/$1/$2/g"

find . -name "$1*" -print0 | xargs -0 rename -S "$1" "$2"
ack --literal --files-with-matches "$1" | xargs sed -i "" "s/$1/$2/g"

find . -name "$1*" -print0 | xargs -0 rename -S "$1" "$2"
ack --literal --files-with-matches "$1" | xargs sed -i "" "s/$1/$2/g"

# double-confirm.  no output means success.
ack --literal "$1"
