import React from 'react'
import CustomDashboard from './custom/Dashboard'

const accounts = require('./views/accounts');
const funds = require('./views/funds');
const nominalAccounts = require('./views/nominalAccounts');
const parishioners = require('./views/parishioners');
const subjects = require('./views/subjects');
const statementItems = require('./views/statementItems');
let { login, logout } = require('./auth')

const admin = {
    id: 'glod',
    title: 'Glod Specialised Ledger',
    options: {
        debug: true,
        basePath: '/crudl-graphql/',
        baseURL: '/graphql/',
    },
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
        dashboard: CustomDashboard
    },
    crudlVersion: "^0.3.0",
    messages: {
        'login.button': 'Sign in',
        'logout.button': 'Sign out',
        'logout.affirmation': 'Have a nice day!',
        'pageNotFound': 'Sorry, page not found.',
    },
};

export default admin
