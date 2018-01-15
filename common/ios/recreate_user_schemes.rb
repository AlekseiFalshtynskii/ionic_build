#!/usr/bin/env ruby
projectName = ARGV[0]
require 'xcodeproj'
xcproj = Xcodeproj::Project.open("platforms/ios/#{projectName}.xcodeproj")
xcproj.recreate_user_schemes
xcproj.save
