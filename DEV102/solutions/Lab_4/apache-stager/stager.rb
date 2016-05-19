#!/usr/bin/env ruby

require "bundler"
Bundler.setup

require "apcera-stager-api"

STDOUT.sync = true

stager = Apcera::Stager.new

# Download the package from the staging coordinator.
puts "Downloading application package..."
stager.download

# Add Apache as dependency
puts "Adding Apache as dependency..."
should_restart = stager.dependencies_add("package", "apache")
if should_restart == true
  stager.relaunch
end

# Extract package to app/ folder.
puts "Extracting package contents..."
stager.extract('app')

# Copy stager's conf/ folder (that contains httpd.conf)
# to the staged app's conf/ folder.
puts "Copying conf folder..."
FileUtils.copy_entry("conf", File.join(stager.app_path, "conf"))

# Add a start command to the app  Apache with custom httpd.conf
start_cmd = "sudo apachectl -f /conf/httpd.conf -DFOREGROUND"
puts "Setting start command to '#{start_cmd}'"
stager.start_command = start_cmd

# Finish staging, this uploads the final package to the staging coordinator.
puts "Uploading package to staging coordinator..."
stager.complete
