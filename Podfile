# Uncomment the next line to define a global platform for your project
platform :ios, '10.2'
source 'https://github.com/CocoaPods/Specs.git'

def developing_pods
    pod 'XCGLogger', '6.0.0'
    pod 'KeychainSwift', '8.0.2'
    pod 'R.swift', '3.3'
    pod 'SnapKit', '4.0'
    pod 'CorePlot', '2.2'
    pod 'ChameleonFramework/Swift', :git => 'https://github.com/ViccAlexander/Chameleon.git'
    pod 'le', '1.1'
    pod 'BugfenderSDK', '1.4.5'
    pod 'JustLog', '1.3'
    pod 'Toast-Swift', '2.0.0'
    pod 'SwiftLint', '0.23'
end

target 'ShareBudget' do
  # Comment the next line if you're not using Swift and don't want to use dynamic frameworks
  use_frameworks!

  # Pods for ShareBudget
  developing_pods
  
  target 'ShareBudgetDevelopmentLocal' do
      inherit! :search_paths
      developing_pods
  end
  
  target 'ShareBudgetDevelopmentRemote' do
      inherit! :search_paths
      developing_pods
  end

  target 'ShareBudgetTests' do
    inherit! :search_paths
    # Pods for testing
    pod 'Nimble', '7.0.2'
  end

  target 'ShareBudgetUITests' do
    inherit! :search_paths
    # Pods for testing
  end
  
  # Manually making compiler version be swift 3.2
  post_install do |installer|
      installer.pods_project.targets.each do |target|
          if target.name == 'JustLog' || target.name == 'Toast-Swift'
              print "\t - Changing "
              print target.name
              print " swift version to 3.2\n"
              target.build_configurations.each do |config|
                  config.build_settings['SWIFT_VERSION'] = '3.2'
              end
          end
      end
  end

end
