//
//  LoginPresenter.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 16.01.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import UIKit
import Rswift
import XCGLogger

enum AuthorisationMode {
    case login
    case signUp
}

protocol LoginPresenterDelegate: BasePresenterDelegate {
    func hideKeyboard()
    func showLogin(title: String)
    func showSignUp(title: String)
    func showAuthorisation(title: String)
    func showError(for field: LoginTextField)
    func hideError(for field: LoginTextField)
    func showKeyboard(for textField: LoginTextField)
    func loginValue(for field: LoginTextField) -> String
    func textType(for textField: UITextField) -> LoginTextField
    func configureTextField(_ textField: LoginTextField, placeholder: String)
}

class LoginPresenter: BasePresenter {
    var mode = AuthorisationMode.login
    weak var delegate: LoginPresenterDelegate?
    
    override func configure() {
        self.updateAthorisationView()
        self.configureLoginTextFields()
    }
    
    // MARK: - Public
    
    func switchAuthorisationMode() {
        if self.mode == .login {
            self.mode = .signUp
        } else {
            self.mode = .login
        }
        
        self.delegate?.hideKeyboard()
        self.updateAthorisationView()
        self.resetAllLoginErrorStatuses()
    }
    
    func authoriseUser() {
        guard let delegate = self.delegate else {
            return
        }
        
        let notValidField = self.findNotValidField()
        
        if notValidField == LoginTextField.none {
            delegate.hideKeyboard()
            
            guard let interaction = self.interaction as? LoginInteraction else {
                return
            }
            
            let email = delegate.loginValue(for: .email(""))
            let password = delegate.loginValue(for: .password(""))
            
            interaction.login(email: email, password: password, completion: { (data: Any, response: URLResponse?, error: Error?) -> (Void) in
                
            })
        }
        else {
            delegate.showError(for: notValidField)
        }
    }
    
    func listenTextFieldChanges(_ textField: UITextField?) {
        textField?.delegate = self
    }
    
    // MARK: - Private
    
    private func resetAllLoginErrorStatuses() {
        self.delegate?.hideError(for: .email(""))
        self.delegate?.hideError(for: .password(""))
        self.delegate?.hideError(for: .repeatPassword(""))
        self.delegate?.hideError(for: .firstName(""))
    }
    
    private func configureLoginTextFields() {
        self.delegate?.configureTextField(.email(""), placeholder: LocalisedManager.login.email)
        self.delegate?.configureTextField(.password(""), placeholder: LocalisedManager.login.password)
        self.delegate?.configureTextField(.repeatPassword(""), placeholder: LocalisedManager.login.repeatPassword)
        self.delegate?.configureTextField(.firstName(""), placeholder: LocalisedManager.login.firstName)
        self.delegate?.configureTextField(.lastName(""), placeholder: LocalisedManager.login.lastName)
    }
    
    private func findNotValidField() -> LoginTextField {
        guard let delegate = self.delegate else {
            return .all
        }
        
        var value = delegate.loginValue(for: .email(""))
        if !Validator.email(value) {
            self.delegate?.showKeyboard(for: .email(""))
            return .email(LocalisedManager.validation.wrongEmailFormat)
        }
        
        value = delegate.loginValue(for: .password(""))
        if !Validator.password(value) {
            self.delegate?.showKeyboard(for: .password(""))
            return .password(LocalisedManager.validation.wrongPasswordFormat)
        }
        
        if self.mode == .login {
            return .none
        }
        
        let password = delegate.loginValue(for: .password(""))
        value = delegate.loginValue(for: .repeatPassword(""))
        if !Validator.repeatPassword(password: password, repeat: value) {
            self.delegate?.showKeyboard(for: .repeatPassword(""))
            return .repeatPassword(LocalisedManager.validation.repeatPasswordIsDifferent)
        }
        
        value = delegate.loginValue(for: .firstName(""))
        if !Validator.firstName(value) {
            self.delegate?.showKeyboard(for: .firstName(""))
            return .firstName(LocalisedManager.validation.firstNameIsEmpty)
        }
        
        return .none
    }
    
    fileprivate func validate(textField: UITextField) {
        guard let input = self.delegate?.textType(for: textField) else {
            return
        }
        
        switch input {
        case let .email(value):
            if !Validator.email(value) {
                self.delegate?.showError(for: .email(LocalisedManager.validation.wrongEmailFormat))
            }
            
        case let .password(value):
            if !Validator.password(value) {
                self.delegate?.showError(for: .password(LocalisedManager.validation.wrongPasswordFormat))
            }
            
        case let .repeatPassword(value):
            guard let delegate = self.delegate else {
                self.delegate?.showError(for: .repeatPassword(LocalisedManager.validation.repeatPasswordIsDifferent))
                return
            }
            
            let password = delegate.loginValue(for: .password(""))
            if !Validator.repeatPassword(password: password, repeat: value) {
                self.delegate?.showError(for: .repeatPassword(LocalisedManager.validation.repeatPasswordIsDifferent))
            }
            
        case let .firstName(value):
            if !Validator.firstName(value) {
                self.delegate?.showError(for: .firstName(LocalisedManager.validation.firstNameIsEmpty))
            }
            
        default:
            break
        }
    }
    
    fileprivate func updateAthorisationView() {
        switch self.mode {
        case .login:
            self.delegate?.showLogin(title: LocalisedManager.login.dontHaveAccount)
            self.delegate?.showPage(title: LocalisedManager.login.title)
            self.delegate?.showAuthorisation(title: LocalisedManager.login.title)
        case .signUp:
            self.delegate?.showSignUp(title: LocalisedManager.login.loginWithExistingAccount)
            self.delegate?.showPage(title: LocalisedManager.login.signUp)
            self.delegate?.showAuthorisation(title: LocalisedManager.login.signUp)
        }
    }
    
    fileprivate func activateNextKeyboard(for textField: UITextField) {
        guard let loginTextField = self.delegate?.textType(for: textField) else {
            return
        }
        
        switch loginTextField {
        case .email(_):
            self.delegate?.showKeyboard(for: .password(""))
            
        case .password(_):
            if self.mode == .login {
                self.authoriseUser()
            }
            else {
                self.delegate?.showKeyboard(for: .repeatPassword(""))
            }
            
        case .repeatPassword(_):
            self.delegate?.showKeyboard(for: .firstName(""))
            
        case .firstName(_):
            self.delegate?.showKeyboard(for: .lastName(""))
            
        case .lastName(_):
            self.authoriseUser()
            
        default:
            break
        }
    }
}

extension LoginPresenter: UITextFieldDelegate {
    func textFieldDidEndEditing(_ textField: UITextField) {
        guard let text = textField.text, text.characters.count > 0 else {
            return
        }
        
        self.validate(textField: textField)
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        self.activateNextKeyboard(for: textField)
        
        return false
    }
    
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
        guard let inputTextField = self.delegate?.textType(for: textField) else {
            return true
        }
        
        self.delegate?.hideError(for: inputTextField)
        
        return true
    }
}
