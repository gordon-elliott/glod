import { optionsFromMap, select } from '../utils'
import React from 'react'

import { organisations } from '../connectors/organisations'

//-------------------------------------------------------------------
const listView = {
    path: 'organisations',
    title: 'Organisations',
    actions: {
        list: function (req) { return organisations.read(req) }
    },
}

const organisationCategoryMap = {
    Household: 'Household',
    NonLocalHousehold: 'NonLocalHousehold',
    Company: 'Company',
    Charity: 'Charity',
    Government: 'Government',
}
let organisationCategories = optionsFromMap(organisationCategoryMap)

const organisationStatusMap = {
    Active: 'Active',
    Inactive: 'Inactive',
}
let organisationStatuses = optionsFromMap(organisationStatusMap)

// id, referenceNo, name, category, status
listView.fields = [
    {
        name: 'referenceNo',
        label: 'Ref. No.',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '4',
        main: true
    },
    {
        name: 'name',
        label: 'Name',
        main: true,
        sortable: true,
        sorted: 'ascending',
        sortpriority: '1',
    },
    {
        name: 'category',
        label: 'Category',
        sortable: true,
        render: value => organisationCategoryMap[value],
    },
    {
        name: 'status',
        label: 'Status',
        sortable: true,
        render: value => organisationStatusMap[value],
    }
]

listView.filters = {
    fields: [
        {
            name: 'referenceNo',
            label: 'Ref. No.',
            field: 'Search',
        },
        {
            name: 'name',
            label: 'Name',
            field: 'Search',
        },
        {
            name: 'category',
            label: 'Category',
            field: 'Select',
            options: organisationCategories
        },
        {
            name: 'status',
            label: 'Status',
            field: 'Select',
            options: organisationStatuses
        }
    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'organisations/:id',
    title: 'Organisation',
    tabtitle: 'Main',
    actions: {
        get: req => organisations(crudl.path.id).read(req),
        delete: req => organisations(crudl.path.id).delete(req),
        save: req => organisations(crudl.path.id).update(req),
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
                name: 'referenceNo',
                label: 'Ref. No.',
                field: 'String',
                required: true,
            },
            {
                name: 'name',
                label: 'Name',
                field: 'String',
                required: true,
            },
            {
                name: 'category',
                label: 'Category',
                field: 'Select',
                options: organisationCategories,
                required: true,
            },
            {
                name: 'status',
                label: 'Status',
                field: 'Select',
                options: organisationStatuses,
                required: true,
            }
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
    path: 'organisations/new',
    title: 'New Organisation',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return organisations.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
