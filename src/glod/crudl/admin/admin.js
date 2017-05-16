import React from 'react'
import CustomDashboard from './custom/Dashboard'

var accounts = require('./views/accounts')
var funds = require('./views/funds')
var nominalAccounts = require('./views/nominalAccounts')
var parishioners = require('./views/parishioners')
var subjects = require('./views/subjects')
var statementItems = require('./views/statementItems')
var connectors = require('./connectors/connectors')
var { login, logout } = require('./auth')

var admin = {
    title: 'Glod Specialised Ledger',
    options: {
        debug: true,
        basePath: '/crudl-graphql/',
        baseURL: '/graphql/',
    },
    connectors,
    views: {
        accounts,
        funds,
        nominalAccounts,
        parishioners,
        subjects,
        statementItems,
    },
    auth: {
        login,
        logout,
    },
    custom: {
        dashboard: <CustomDashboard />,
    },
    messages: {
        'login.button': 'Sign in',
        'logout.button': 'Sign out',
        'logout.affirmation': 'Have a nice day!',
        'pageNotFound': 'Sorry, page not found.',
    },
}

export default admin
