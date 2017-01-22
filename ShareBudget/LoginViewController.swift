//
//  LoginViewController.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 16.01.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import UIKit

class LoginViewController: BaseViewController {
    @IBOutlet private var stackView: UIStackView?
    @IBOutlet private var emailTextField: UITextField?
    @IBOutlet private var authorisationButton: UIButton?
    @IBOutlet private var passwordTextField: UITextField?
    @IBOutlet private var lastNameTextField: UITextField?
    @IBOutlet private var firstNameTextField: UITextField?
    @IBOutlet private var authorisationModeButton: UIButton?
    @IBOutlet private var repeatPasswordTextField: UITextField?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let router = LoginRouter(with: self)
        let interactin = LoginInteraction(with: router)
        let presenter = LoginPresenter(with: interactin)
        self.viperView = LoginView(with: presenter, and: self)
        
        guard let view = self.viperView as? LoginView else {
            return
        }
        
        self.linkStoryboardViews(to: view)
        self.linkViewActions(to: presenter)
        
        presenter.configure()
    }

    private func linkStoryboardViews(to view: LoginView) {
        view.stackView = self.stackView
        view.emailTextField = self.emailTextField
        view.lastNameTextField = self.lastNameTextField
        view.passwordTextField = self.passwordTextField
        view.firstNameTextField = self.firstNameTextField
        view.authorisationButton = self.authorisationButton
        view.repeatPasswordTextField = self.repeatPasswordTextField
        view.authorisationModeButton = self.authorisationModeButton
    }
    
    private func linkViewActions(to presenter: LoginPresenter) {
        presenter.listenTextFieldChanges(self.emailTextField)
        presenter.listenTextFieldChanges(self.passwordTextField)
        presenter.listenTextFieldChanges(self.lastNameTextField)
        presenter.listenTextFieldChanges(self.firstNameTextField)
        presenter.listenTextFieldChanges(self.repeatPasswordTextField)
        
        self.authorisationButton?.addTarget(presenter, action: #selector(LoginPresenter.authoriseUser), for: .touchUpInside)
        self.authorisationModeButton?.addTarget(presenter, action: #selector(LoginPresenter.switchAuthorisationMode), for: .touchUpInside)
    }
}
