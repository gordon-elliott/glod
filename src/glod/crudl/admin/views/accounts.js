import React from 'react'

import { accounts } from '../connectors/accounts'
import {funds} from "../connectors/funds";

//-------------------------------------------------------------------
const listView = {
    path: 'accounts',
    title: 'Accounts',
    actions: {
        list: function (req) { return accounts.read(req) },
    },
};

// id, referenceNo, purpose, status, name, institution, sortCode, accountNo, BIC, IBAN
listView.fields = [
    {
        name: 'referenceNo',
        label: 'Ref. No',
        main: true,
        sortable: true,
        sorted: 'ascending',
        sortpriority: '1',
    },
    {
        name: 'purpose',
        label: 'Purpose',
        sortable: true,
    },
    {
        name: 'status',
        label: 'Status',
        sortable: true,
    },
    {
        name: 'name',
        label: 'Name',
        main: true,
        sortable: true,
    },
    {
        name: 'institution',
        label: 'Institution',
        sortable: true,
    },
    {
        name: 'accountNo',
        label: 'Account No',
        sortable: true,
    },
    {
        name: 'IBAN',
        label: 'IBAN',
        sortable: true,
    },
]

listView.filters = {
    fields: [
        {
            name: 'referenceNo',
            label: 'Ref. No',
            field: 'Search',
        },
        {
            name: 'purpose',
            label: 'Purpose',
            field: 'Search',
        },
        {
            name: 'status',
            label: 'Status',
            field: 'Select',
            options: [
                {value: 'Active', label: 'Active'},
                {value: 'Closed', label: 'Closed'}
            ],
        },
        {
            name: 'name',
            label: 'Name',
            field: 'Search',
        },
        {
            name: 'institution',
            label: 'Institution',
            field: 'Search',
        },
        {
            name: 'accountNo',
            label: 'Account No',
            field: 'Search',
        },
        {
            name: 'IBAN',
            label: 'IBAN',
            field: 'Search',
        },
    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'accounts/:id',
    title: 'Account',
    tabtitle: 'Main',
    actions: {
        get: req => accounts(crudl.path.id).read(req),
        delete: req => accounts(crudl.path.id).delete(req),
        save: req => accounts(crudl.path.id).update(req),
    },
    validate: function (values) {
        if (!values.name || values.name == "") {
            return {_error: '`Name` is required.'}
        }
    },
    denormalize: function (data) {
        /* prevent unknown field ... with query */
        delete(data.updatedate)
        delete(data.owner)
        delete(data.createdate)
        return data
    },
};

changeView.fieldsets = [
    {
        fields: [
            {
                name: 'id',
                field: 'hidden',
            },
            {
                name: 'referenceNo',
                label: 'Ref. No',
                field: 'String',
                readOnly: true,
            },
            {
                name: 'purpose',
                label: 'Purpose',
                field: 'String',
            },
            {
                name: 'status',
                label: 'Status',
                field: 'Select',
                required: true,
                initialValue: 'Active',
                /* set options manually */
                options: [
                    {value: 'Active', label: 'Active'},
                    {value: 'Closed', label: 'Closed'}
                ],
            },
            {
                name: 'name',
                label: 'Name',
                field: 'String',
            },
        ],
    },
    {
        title: 'Bank details',
        expanded: true,
        fields: [
            {
                name: 'institution',
                label: 'Institution',
                field: 'String',
            },
            {
                name: 'IBAN',
                label: 'IBAN',
                field: 'String',
            },
            {
                name: 'sortCode',
                label: 'Sort Code',
                field: 'String',
            },
            {
                name: 'accountNo',
                label: 'Account No',
                field: 'String',
            },
        ]
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
    path: 'accounts/new',
    title: 'New Account',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return accounts.create(req) },
    },
};

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
