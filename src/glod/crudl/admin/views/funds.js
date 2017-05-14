import { optionsFromMap } from '../utils'
import React from 'react'

//-------------------------------------------------------------------
var listView = {
    path: 'funds',
    title: 'Funds',
    actions: {
        list: function (req) {
            let funds = crudl.connectors.funds.read(req)
            return funds
        }
    },
}

const fundMap = {
    Unrestricted: 'Unrestricted',
    Restricted: 'Restricted',
    Endowment: 'Endowment',
}
let fundOptions = optionsFromMap(fundMap)


// id, name, type, isParishFund, account
listView.fields = [
    {
        name: 'name',
        label: 'Name',
        main: true,
        sortable: true,
        sorted: 'ascending',
        sortpriority: '1',
    },
    {
        name: 'type',
        label: 'Type',
        sortable: true,
        render: value => fundMap[value],
    },
    {
        name: 'isParishFund',
        label: 'Is Parish Fund?',
        render: 'boolean',
    },
    {
        name: 'account',
        key: 'account.name',
        label: 'Account',
        sortable: true,
    },
]

listView.filters = {
    fields: [
        {
            name: 'name',
            label: 'Name',
            field: 'Search',
        },
        {
            name: 'type',
            label: 'Type',
            field: 'Select',
            props: {
                options: fundOptions
            }
        },
        {
            name: 'isParishFund',
            label: 'Is Parish Fund?',
            field: 'Select',
            props: {
                options: [
                    {value: 'true', label: 'True'},
                    {value: 'false', label: 'False'}
                ],
                helpText: 'Note: We use Select in order to distinguish false and none.'
            }
        },
        {
            name: 'account',
            label: 'Account',
            field: 'Select',
            props: () => crudl.connectors.accountsOptions.read(crudl.req()).then(res => res.data),
        },
    ]
}

//-------------------------------------------------------------------
var changeView = {
    path: 'funds/:id',
    title: 'Fund',
    tabtitle: 'Main',
    actions: {
        get: function (req) { return crudl.connectors.fund(crudl.path.id).read(req) },
        save: function (req) { return crudl.connectors.fund(crudl.path.id).update(req) },
    },
    validate: function (values) {
        if (!values.name || values.name == "") {
            return { _error: '`Name` is required.' }
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
                name: 'name',
                label: 'Name',
                field: 'String',
            },
            {
                name: 'type',
                label: 'Type',
                field: 'Select',
                required: true,
                props: {
                    options: fundOptions
                },
            },
            {
                name: 'isParishFund',
                label: 'Is Parish Fund?',
                field: 'Checkbox',
            },
            {
                name: 'account',
                key: 'account.id',
                label: 'Account',
                field: 'Select',
                props: () => crudl.connectors.accountsOptions.read(crudl.req()).then(res => ({
                    helpText: 'Select an account',
                    ...res.data
                }))
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
    path: 'funds/new',
    title: 'New Fund',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return crudl.connectors.funds.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
