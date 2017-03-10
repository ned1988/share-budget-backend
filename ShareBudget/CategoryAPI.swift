//
//  CategoryAPI.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 08.02.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import CoreData
import XCGLogger

class CategoryAPI: BaseAPI {
    override class func modelKeyID() -> String {
        return kCategoryID
    }
    
    override class func timestampStorageKey() -> String {
        return "category_timestamp"
    }
    
    override class func parseUpdates(items: [[String: AnyObject?]], in managedObjectContext: NSManagedObjectContext) {
        var category: Category?
        
        for item in items {
            if let modelID = item[self.modelKeyID()] as? Int {
                category = ModelManager.findEntity(Category.self, by: modelID, in: managedObjectContext) as? Category
            }
            
            if category == nil {
                category = Category(context: managedObjectContext)
            }
            
            category?.update(with: item, in: managedObjectContext)
        }
    }
    
    override class func allChangedModels(completionBlock: APIResultBlock?) -> [BaseAPITask] {
        let managedObjectContext = ModelManager.managedObjectContext
        let fetchedResultsController = ModelManager.changedModels(Category.self ,managedObjectContext)
        
        var tasks = [BaseAPITask]()
        
        let sections = fetchedResultsController?.sections ?? []
        for i in 0..<sections.count {
            let section = sections[i]
            for j in 0..<section.numberOfObjects {
                let indexPath = IndexPath(row: j, section: i)
                guard let model = fetchedResultsController?.object(at: indexPath) as? Category else {
                    continue
                }
                
                let modelID = model.objectID
                let task = BaseAPITaskUpload(resource: "category", entity: CategoryAPI.self, modelID: modelID, completionBlock: completionBlock)
                tasks.append(task)
            }
        }
        
        return tasks
    }
}
