import {optionsFromMap, select} from '../utils'
import React from 'react'

import { statementItems } from '../connectors/statementItems'
import { accountOptions } from '../connectors/accounts'

//-------------------------------------------------------------------
const listView = {
    path: 'statementItems',
    title: 'Statement Items',
    actions: {
        list: function (req) { return statementItems.read(req) }
    },
}

// id, account, date, details, currency, debit, credit, balance
listView.fields = [
    {
        name: 'account',
        getValue: select('account.name'),
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
            props: () => accountOptions.read(crudl.req()).then(res => res.data),
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
const changeView = {
    path: 'statementItems/:id',
    title: 'Statement Item',
    tabtitle: 'Main',
    actions: {
        get: req => statementItems(crudl.path.id).read(req),
        delete: req => statementItems.delete(req), // the request contains the id already
        save: req => statementItems.update(req), // the request contains the id already
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
                getValue: select('account.id'),
                label: 'Account',
                field: 'Select',
                lazy: () => accountOptions.read(crudl.req()).then(res => ({
                    helpText: 'Select an account',
                    ...res
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
const addView = {
    path: 'statementItems/new',
    title: 'New Statement Item',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return statementItems.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
