//
//  User+CoreDataProperties.swift
//  
//
//  Created by Denys Meloshyn on 29.01.17.
//
//

import Foundation
import CoreData


extension User {

    @nonobjc public class func fetchRequest() -> NSFetchRequest<User> {
        return NSFetchRequest<User>(entityName: "User");
    }

    @NSManaged public var email: String?
    @NSManaged public var firstName: String?
    @NSManaged public var lastName: String?
    @NSManaged public var group: Budget?

}