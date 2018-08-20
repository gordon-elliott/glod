import { optionsFromMap, select } from '../utils'
import React from 'react'

import { funds } from '../connectors/funds'
import { accountOptions } from '../connectors/accounts'

//-------------------------------------------------------------------
const listView = {
    path: 'funds',
    title: 'Funds',
    actions: {
        list: function (req) { return funds.read(req) }
    },
}

const fundRestrictionMap = {
    Unrestricted: 'Unrestricted',
    Restricted: 'Restricted',
    Endowment: 'Endowment'
}
let fundRestrictions = optionsFromMap(fundRestrictionMap)

// id, name, restriction, isParishFund, account
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
        name: 'restriction',
        label: 'Restriction',
        sortable: true,
        render: value => fundRestrictionMap[value],
    },
    {
        name: 'isParishFund',
        label: 'Is Parish Fund?',
        render: 'boolean',
    },
    {
        name: 'account',
        getValue: select('account.name'),
        label: 'Account',
        sortable: true,
    },
]

listView.filters = {
    denormalize: function (frontend) {
        if (frontend.hasOwnProperty('isParishFund')) {
            frontend.isParishFund = frontend.isParishFund === 'true';
        }
        return frontend;
    },
    fields: [
        {
            name: 'name',
            label: 'Name',
            field: 'Search',
        },
        {
            name: 'restriction',
            label: 'Restriction',
            field: 'Select',
            options: fundRestrictions
        },
        {
            name: 'isParishFund',
            label: 'Is Parish Fund?',
            field: 'Select',
            options: [
                {value: 'true', label: 'True'},
                {value: 'false', label: 'False'}
            ],
            helpText: 'Note: We use Select in order to distinguish false and none.'
        },
        {
            name: 'account',
            label: 'Account',
            field: 'Select',
            lazy: () => accountOptions.read(crudl.req()).then(res => ({
                helpText: 'Select an account',
                ...res
            })),
        },
    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'funds/:id',
    title: 'Fund',
    tabtitle: 'Main',
    actions: {
        get: req => funds(crudl.path.id).read(req),
        delete: req => funds.delete(req), // the request contains the id already
        save: req => funds.update(req), // the request contains the id already
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
                name: 'restriction',
                label: 'Restriction',
                field: 'Select',
                required: true,
                options: fundRestrictions
            },
            {
                name: 'isParishFund',
                label: 'Is Parish Fund?',
                field: 'Checkbox',
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
        add: function (req) { return funds.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
