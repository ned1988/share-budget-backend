//
//  BudgetDetailPresenter.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 03.02.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import CorePlot

protocol BudgetDetailPresenterDelegate: BasePresenterDelegate {
    func updateBalance(_ balance: String)
    func updateMonthLimit(_ limit: String)
    func updateTotalExpense(_ total: String)
    func updateCurrentMonthDate(_ date: String)
    func updateExpenseCoverColor(_ color: UIColor?)
}

class BudgetDetailPresenter: BasePresenter {
    weak var delegate: BudgetDetailPresenterDelegate?
    
    private var colorsRange = [Range<Double>]()
    private let colors = [UIColor.green, UIColor.yellow, UIColor.red]
    
    fileprivate var budgetDetailInteraction: BudgetDetailInteraction {
        get {
            return self.interaction as! BudgetDetailInteraction
        }
    }
    
    private var budgetDetailRouter: BudgetDetailRouter {
        get {
            return self.router as! BudgetDetailRouter
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.delegate?.showPage(title: self.budgetDetailInteraction.budget.name)
        self.delegate?.updateCurrentMonthDate(UtilityFormatter.yearMonthFormatter.string(from: Date()))
        self.configureColors()
        self.configureTotalExpenses()
        self.configureMonthBudget()
        self.configureBalance()
        self.updateTotalSpentExpensesColor()
    }
    
    private func configureColors() {
        let rangeLength = 1.0 / Double(self.colors.count)
        
        for i in 0..<colors.count {
            let start = rangeLength * Double(i)
            let end = rangeLength * Double(i + 1)
            
            self.colorsRange.append(start..<end)
        }
    }
    
    private func updateTotalSpentExpensesColor() {
        let budget = self.budgetDetailInteraction.lastMonthLimit()?.limit ?? 0.0
        
        let totalExpenses = self.budgetDetailInteraction.totalExpenses()
        
        if totalExpenses == 0.0 {
            self.delegate?.updateExpenseCoverColor(self.colors.first)
            return
        }
        
        if budget == 0.0 {
            self.delegate?.updateExpenseCoverColor(self.colors.last)
            return
        }
        
        let percent = totalExpenses / budget
        let percentColor = Double(colors.count) * percent
        let percentColorIndex = Int(floor(percentColor))
        
        if percentColorIndex == 0 {
            let resColor = colors[percentColorIndex]
            self.delegate?.updateExpenseCoverColor(resColor)
        }
        else if percentColorIndex == colors.count {
            let resColor = colors.last
            self.delegate?.updateExpenseCoverColor(resColor)
        }
        else {
            for range in colorsRange {
                if range.contains(percent) {
                    guard let rangeIndex = colorsRange.index(of: range) else {
                        continue
                    }
                    
                    let dif = percent - range.lowerBound
                    let rangeLength = range.upperBound - range.lowerBound
                    let rangePercantage = dif / rangeLength
                    
                    let fromColor = colors[rangeIndex - 1]
                    let toColor = colors[rangeIndex]
                    
                    let cgiColors = fromColor.cgColor.components ?? []
                    var resCGIColors = [Float]()
                    for i in 0..<cgiColors.count {
                        let toColorValue = toColor.cgColor.components![i]
                        let fromColorValue = cgiColors[i]
                        let resValue = (Double(toColorValue) - Double(fromColorValue)) * rangePercantage + Double(fromColorValue)
                        resCGIColors.append(Float(resValue))
                    }
                    
                    let resColor = UIColor(colorLiteralRed: resCGIColors[0], green: resCGIColors[1], blue: resCGIColors[2], alpha: resCGIColors[3])
                    self.delegate?.updateExpenseCoverColor(resColor)
                }
            }
        }
    }
    
    private func configureTotalExpenses() {
        let total = self.budgetDetailInteraction.totalExpenses()
        self.delegate?.updateTotalExpense(String(total))
    }
    
    private func configureMonthBudget() {
        let month = self.budgetDetailInteraction.lastMonthLimit()
        self.delegate?.updateMonthLimit(String(month?.limit ?? 0.0))
    }
    
    private func configureBalance() {
        self.delegate?.updateBalance(String(self.budgetDetailInteraction.balance()))
    }
    
    func createNewExpense() {
        self.budgetDetailRouter.openEditExpensePage(with: self.budgetDetailInteraction.budgetID)
    }
    
    func showAllExpenses() {
        self.budgetDetailRouter.showAllExpensesPage(with: self.budgetDetailInteraction.budgetID)
    }
}

// MARK: - CPTPieChartDataSource

extension BudgetDetailPresenter: CPTPieChartDataSource {
    func numberOfRecords(for plot: CPTPlot) -> UInt {
        if self.budgetDetailInteraction.isEmpty() {
            return 1
        }
        
        return UInt(self.budgetDetailInteraction.numberOfCategoryExpenses())
    }
    
    func number(for plot: CPTPlot, field: UInt, record: UInt) -> Any? {
        if self.budgetDetailInteraction.isEmpty() {
            return 1 as NSNumber
        }
        
        switch CPTPieChartField(rawValue: Int(field))! {
        case .sliceWidth:
            return NSNumber(value: self.budgetDetailInteraction.totalExpenses(for: Int(record)))
            
        default:
            return record as NSNumber
        }
    }
    
    func dataLabel(for plot: CPTPlot, record: UInt) -> CPTLayer? {
        if self.budgetDetailInteraction.isEmpty() {
            return nil
        }
        
        let label = CPTTextLayer(text:self.budgetDetailInteraction.categoryTitle(for: Int(record)))
        
        if let textStyle = label.textStyle?.mutableCopy() as? CPTMutableTextStyle {
            textStyle.color = .lightGray()
            
            label.textStyle = textStyle
        }
        
        return label
    }
    
    func sliceFill(for pieChart: CPTPieChart, record idx: UInt) -> CPTFill? {
        if self.budgetDetailInteraction.isEmpty() {
            return CPTFill(color: CPTColor.gray())
        }
        
        return nil
    }
}

// MARK: - CPTPieChartDelegate

extension BudgetDetailPresenter: CPTPieChartDelegate {
    func pieChart(_ plot: CPTPieChart, sliceTouchDownAtRecord idx: UInt) {
        
    }
}
