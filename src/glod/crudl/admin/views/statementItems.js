import { optionsFromMap } from '../utils'
import React from 'react'

//-------------------------------------------------------------------
var listView = {
    path: 'statementItems',
    title: 'Statement Items',
    actions: {
        list: function (req) {
            let statementItems = crudl.connectors.statementItems.read(req)
            return statementItems
        }
    },
}

// id, account, date, details, currency, debit, credit, balance
listView.fields = [
    {
        name: 'account',
        key: 'account.name',
        label: 'Account',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '1',
    },
    {
        name: 'date',
        label: 'Book date',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '2',
    },
    {
        name: 'details',
        label: 'Details',
        main: true,
        sortable: true,
    },
    {
        name: 'currency',
        label: 'Currency',
    },
    {
        name: 'debit',
        label: 'Debit',
        render: 'number',
    },
    {
        name: 'credit',
        label: 'Credit',
        render: 'number',
    },
    {
        name: 'balance',
        label: 'Balance',
        render: 'number',
    },
]

listView.filters = {
    fields: [
        {
            name: 'account',
            label: 'Account',
            field: 'Select',
            props: () => crudl.connectors.accountsOptions.read(crudl.req()).then(res => res.data),
        },
        {
            name: 'date',
            label: 'Book date',
            field: 'Date',
        },
        {
            name: 'details',
            label: 'Details',
            field: 'Search',
        },
        {
            name: 'debit',
            label: 'Debit',
            field: 'Search',
        },
        {
            name: 'credit',
            label: 'Credit',
            field: 'Search',
        },

    ]
}

//-------------------------------------------------------------------
var changeView = {
    path: 'statementItems/:id',
    title: 'Statement Item',
    tabtitle: 'Main',
    actions: {
        get: function (req) { return crudl.connectors.statementItem(crudl.path.id).read(req) },
        save: function (req) { return crudl.connectors.statementItem(crudl.path.id).update(req) },
    },
    validate: function (values) {
        if (!values.account || values.account == "") {
            return { _error: '`Account` is required.' }
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
                name: 'account',
                key: 'account.id',
                label: 'Account',
                field: 'Select',
                props: () => crudl.connectors.accountsOptions.read(crudl.req()).then(res => ({
                    helpText: 'Select an account',
                    ...res.data
                })),
                required: true,
            },
            {
                name: 'date',
                label: 'Book date',
                field: 'Date',
                required: true,
            },
            {
                name: 'details',
                label: 'Details',
                field: 'String',
                required: true,
            },
            {
                name: 'currency',
                label: 'Currency',
                field: 'String',
                initialValue: 'EUR',
                required: true,
            },
            {
                name: 'debit',
                label: 'Debit',
                field: 'String',
            },
            {
                name: 'credit',
                label: 'Credit',
                field: 'String',
            },
            {
                name: 'balance',
                label: 'Balance',
                field: 'String',
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
var addView = {
    path: 'statementItems/new',
    title: 'New Statement Item',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return crudl.connectors.statementItems.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
