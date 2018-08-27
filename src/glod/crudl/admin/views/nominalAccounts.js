import { optionsFromMap } from '../utils'
import React from 'react'

import { nominalAccounts } from '../connectors/nominalAccounts'
import {funds} from "../connectors/funds";


const listView = {
    path: 'nominalAccounts',
    title: 'Nominal Accounts',
    actions: {
        list: function (req) { return nominalAccounts.read(req) }
    },
}

const SOFAHeadingMap = {
    Donations_and_legacies: 'Donations and legacies',
    Income_from_charitable_activities: 'Income from charitable activities',
    Other_trading_activities: 'Other trading activities',
    Investments: 'Investments',
    Other_income: 'Other income',
    Raising_funds: 'Raising funds',
    Expenditure_on_charitable_activities: 'Expenditure on charitable activities',
    Other_expenditure: 'Other expenditure',
}
let SOFAHeadingOptions = optionsFromMap(SOFAHeadingMap)

const categoryMap = {
    Income: 'Income',
    Expenditure: 'Expenditure',
    Fixed_assets: 'Fixed assets',
    Current_assets: 'Current assets',
    Liabilities: 'Liabilities',
}
let categoryOptions = optionsFromMap(categoryMap)

const subCategoryMap = {
    Tangible_assets: 'Tangible assets',
    Investments: 'Investments',
    Debtors: 'Debtors',
    Cash_at_bank_and_in_hand: 'Cash at bank and in hand',
    Creditors_Amounts_falling_due_in_one_year: 'Creditors - Amounts falling due in one year',
    Creditors_Amounts_falling_due_after_more_than_one_year: 'Creditors - Amounts falling due after more than one year',
    Agency_accounts: 'Agency accounts',
    Reserves: 'Reserves',
}
let subCategoryOptions = optionsFromMap(subCategoryMap)

// id, code, description, SOFAHeading, category, subCategory
listView.fields = [
    {
        name: 'code',
        label: 'Code',
        main: true,
        sortable: true,
        sorted: 'ascending',
        sortpriority: '1',
    },
    {
        name: 'description',
        label: 'Description',
        sortable: true,
    },
    {
        name: 'SOFAHeading',
        label: 'SOFA Heading',
        sortable: true,
        render: value => SOFAHeadingMap[value],
    },
    {
        name: 'category',
        label: 'Category',
        main: true,
        sortable: true,
        render: value => categoryMap[value],
    },
    {
        name: 'subCategory',
        label: 'Sub-category',
        sortable: true,
        render: value => subCategoryMap[value],
    },
]


listView.filters = {
    fields: [
        {
            name: 'code',
            label: 'Code',
            field: 'Search',
        },
        {
            name: 'description',
            label: 'Description',
            field: 'Search',
        },
        {
            name: 'SOFAHeading',
            label: 'SOFA Heading',
            field: 'Select',
            options: SOFAHeadingOptions,
        },
        {
            name: 'category',
            label: 'Category',
            field: 'Select',
            options: categoryOptions,
        },
        {
            name: 'subCategory',
            label: 'Sub-category',
            field: 'Select',
            options: subCategoryOptions,
        },
    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'nominalAccounts/:id',
    title: 'Account',
    tabtitle: 'Main',
    actions: {
        get: req => nominalAccounts(crudl.path.id).read(req),
        delete: req => nominalAccounts(crudl.path.id).delete(req),
        save: req => nominalAccounts(crudl.path.id).update(req),
    },
    validate: function (values) {
        if (!values.code || values.code == "") {
            return { _error: '`Code` is required.' }
        }
    },
    denormalize: function (data) {
        /* prevent unknown field ... with query */
        delete(data.updatedate)
        delete(data.owner)
        delete(data.createdate)
        return data
    },
}

changeView.fieldsets = [
    {
        fields: [
            {
                name: 'id',
                field: 'hidden',
            },
            {
                name: 'code',
                label: 'Code',
                field: 'String',
            },
            {
                name: 'description',
                label: 'Description',
                field: 'String',
            },
            {
                name: 'SOFAHeading',
                label: 'SOFA Heading',
                field: 'Select',
                options: SOFAHeadingOptions
            },
            {
                name: 'category',
                label: 'Category',
                field: 'Select',
                options: categoryOptions
            },
            {
                name: 'subCategory',
                label: 'Sub-category',
                field: 'Select',
                options: subCategoryOptions
            },
        ],
    },
    {
        title: 'Internal',
        expanded: false,
        fields: [
            {
                name: 'createdate',
                label: 'Date (Create)',
                field: 'Datetime',
                props: { disabled: true },
            },
            {
                name: 'updatedate',
                label: 'Date (Update)',
                field: 'Datetime',
                props: { disabled: true },
            },
        ]
    }
]

//-------------------------------------------------------------------
const addView = {
    path: 'nominalAccounts/new',
    title: 'New Nominal Account',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return nominalAccounts.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
