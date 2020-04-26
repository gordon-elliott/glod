import { optionsFromMap, select } from '../utils'
import React from 'react'

import { addresses } from '../connectors/addresses'
import { accountOptions } from '../connectors/accounts'

//-------------------------------------------------------------------
const listView = {
    path: 'addresses',
    title: 'Addresses',
    actions: {
        list: function (req) { return addresses.read(req) }
    },
}

// id, address1, address2, address3, county, countryISO, eircode, telephone
listView.fields = [
    {
        name: 'address1',
        label: 'Address line 1',
        main: true,
        sortable: true,
        sorted: 'ascending',
        sortpriority: '5',
    },
    {
        name: 'address2',
        label: 'Address line 2',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '4',
    },
    {
        name: 'address3',
        label: 'Address line 3',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '3',
    },
    {
        name: 'county',
        label: 'County',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '2',
    },
    {
        name: 'countryISO',
        label: 'Country Code',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '1',
    },
    {
        name: 'eircode',
        label: 'Post code',
        sortable: true,
    },
    {
        name: 'telephone',
        label: 'Telephone',
        sortable: true,
    },
]

listView.filters = {
    fields: [
        {
            name: 'address1',
            label: 'Address line 1',
            field: 'Search',
        },
        {
            name: 'address2',
            label: 'Address line 2',
            field: 'Search',
        },
        {
            name: 'address3',
            label: 'Address line 3',
            field: 'Search',
        },
        {
            name: 'county',
            label: 'County',
            field: 'Search',
        },
        {
            name: 'countryISO',
            label: 'Country Code',
            field: 'Search',
        },
        {
            name: 'eircode',
            label: 'Post code',
            field: 'Search',
        },
        {
            name: 'telephone',
            label: 'Telephone',
            field: 'Search',
        },
    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'addresses/:id',
    title: 'Address',
    tabtitle: 'Main',
    actions: {
        get: req => addresses(crudl.path.id).read(req),
        delete: req => addresses(crudl.path.id).delete(req),
        save: req => addresses(crudl.path.id).update(req),
    },
    validate: function (values) {
        if (!values.address1 || values.address1 == "") {
            return { _error: '`Address Line 1` is required.' }
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
                name: 'address1',
                label: 'Address line 1',
                field: 'String',
            },
            {
                name: 'address2',
                label: 'Address line 2',
                field: 'String',
            },
            {
                name: 'address3',
                label: 'Address line 3',
                field: 'String',
            },
            {
                name: 'county',
                label: 'County',
                field: 'String',
            },
            {
                name: 'countryISO',
                label: 'Country Code',
                field: 'String',
            },
            {
                name: 'eircode',
                label: 'Post code',
                field: 'String',
            },
            {
                name: 'telephone',
                label: 'Telephone',
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
    path: 'addresses/new',
    title: 'New Address',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return addresses.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
