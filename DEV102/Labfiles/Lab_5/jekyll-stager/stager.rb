#!/usr/bin/env ruby

require "bundler"
Bundler.setup

require "apcera-stager-api"

STDOUT.sync = true

stager = Apcera::Stager.new

# Download the package from the staging coordinator.
puts "Downloading application package..."
stager.download

# Extract the package contents (Jekyll project file)
puts "Extracting package contents..."
stager.extract('app')

# Install Jekyll dependencies
puts "Installing dependencies..."
stager.execute_app("bundle install --path ../site-vendor/bundle --binstubs ../site-vendor/bundle/bin --deployment")

# Set some environment variables to help Ruby handle file encoding
ENV["LC_ALL"] = "en_US.UTF-8"
ENV["LANG"] = "en_US.UTF-8"

# Build the site with Jekyll
puts "Building the site..."
stager.execute_app("../site-vendor/bundle/bin/jekyll build --trace")

# Jekyll puts the generated web site files in a folder named "_site".
# This tells the stager library to upload that folder's contents.
stager.app_path = "/tmp/staging/app/_site"

# Upload the final package (static site file) to the staging coordinator.
puts "Staging complete, uploading package to staging coordinator."
stager.complete