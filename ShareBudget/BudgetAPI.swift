//
//  BudgetAPI.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 30.01.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import CoreData
import XCGLogger

class BudgetAPI: BaseAPI {
    override class func modelKeyID() -> String {
        return kGroupID
    }
    
    override class func timestampStorageKey() -> String {
        return "budget_timestamp"
    }
    
    override class func parseUpdates(items: [[String: AnyObject?]], in managedObjectContext: NSManagedObjectContext) {
        var budget: Budget?
        
        for item in items {
            if let internalID = item[kInternalID] as? Int {
                budget = ModelManager.findEntity(Budget.self, internal: internalID, in: managedObjectContext) as? Budget
            } else if let modelID = item[BudgetAPI.modelKeyID()] as? Int {
                budget = ModelManager.findEntity(Budget.self, by: modelID, in: managedObjectContext) as? Budget
            }
            
            if budget == nil {
                budget = Budget(context: managedObjectContext)
            }
            
            budget?.update(with: item, in: managedObjectContext)
        }
    }
    
    override class func allChangedModels(completionBlock: APIResultBlock?) -> [BaseAPITask] {
        let managedObjectContext = ModelManager.managedObjectContext
        let fetchedResultsController = ModelManager.changedModels(Budget.self ,managedObjectContext)
        
        var tasks = [BaseAPITask]()
        
        let sections = fetchedResultsController?.sections ?? []
        for i in 0..<sections.count {
            let section = sections[i]
            for j in 0..<section.numberOfObjects {
                let indexPath = IndexPath(row: j, section: i)
                guard let model = fetchedResultsController?.object(at: indexPath) as? Budget else {
                    continue
                }
                
                let task = BaseAPITaskUpload(resource: "group", entity: BudgetAPI.self, modelID: model.objectID, completionBlock: completionBlock)
                tasks.append(task)
            }
        }
        
        return tasks
    }
}