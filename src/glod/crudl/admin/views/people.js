import {formatDate, optionsFromMap, select} from '../utils'
import React from 'react'

import { people } from '../connectors/people'
import { organisationOptions } from "../connectors/organisations";

const personStatusMap = {
    Active: 'Active',
    Inactive: 'Inactive',
}
let personStatuses = optionsFromMap(personStatusMap)


//-------------------------------------------------------------------
const listView = {
    path: 'people',
    title: 'People',
    actions: {
        list: function (req) { return people.read(req) }
    },
}

//  id, organisation{id, name}, familyName, givenName, status, title, mobile, email, dateOfBirth, dobIsEstimate
listView.fields = [
    {
        name: 'organisation',
        getValue: select('organisation.referenceNo'),
        label: 'Organisation',
        sortable: true,
    },
    {
        name: 'title',
        label: 'Title',
        sortable: true,
    },
    {
        name: 'givenName',
        label: 'Given Name',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '3',
    },
    {
        name: 'familyName',
        label: 'Family Name',
        sortable: true,
        sorted: 'ascending',
        sortpriority: '2',
        main: true,
    },
    {
        name: 'status',
        label: 'Status',
        sortable: true,
        render: value => personStatusMap[value],
        sorted: 'ascending',
        sortpriority: '1',
    },
    {
        name: 'mobile',
        label: 'Mobile',
        sortable: true,
    },
    {
        name: 'email',
        label: 'Email',
        sortable: true,
    },
    {
        name: 'dateOfBirth',
        label: 'Date of birth',
        sortable: true,
    },
    {
        name: 'dobIsEstimate',
        label: 'DoB Is Estimate',
        sortable: false,
    },
]

listView.filters = {
    denormalize: function (frontend) {
        if (frontend.hasOwnProperty('dobIsEstimate')) {
            frontend.dobIsEstimate = frontend.dobIsEstimate === 'true';
        }
        return frontend;
    },
    fields: [
        {
            name: 'organisation',
            label: 'Organisation',
            field: 'Select',
            lazy: () => organisationOptions.read(crudl.req()).then(res => ({
                helpText: 'Select an account',
                ...res
            })),
        },
        {
            name: 'title',
            label: 'Title',
            field: 'Search',
        },
        {
            name: 'givenName',
            label: 'Given Name',
            field: 'Search',
        },
        {
            name: 'familyName',
            label: 'Family Name',
            field: 'Search',
        },
        {
            name: 'status',
            label: 'Status',
            field: 'Select',
            options: personStatuses
        },
        {
            name: 'mobile',
            label: 'Mobile',
            field: 'Search',
        },
        {
            name: 'email',
            label: 'Email',
            field: 'Search',
        },
        {
            name: 'dateOfBirth',
            label: 'Date of birth',
            field: 'Date',
        },
        {
            name: 'dobIsEstimate',
            label: 'DoB Is Estimate',
            field: 'Select',
            options: [
                {value: 'true', label: 'True'},
                {value: 'false', label: 'False'}
            ],
            helpText: 'Is the date of birth an exact date or estimate?'
        },
    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'parishioners/:id',
    title: 'Parishioners',
    tabtitle: 'Main',
    actions: {
        get: req => parishioners(crudl.path.id).read(req),
        delete: req => parishioners.delete(req), // the request contains the id already
        save: req => parishioners.update(req), // the request contains the id already
    },
    validate: function (values) {
        if (!values.surname || values.surname == "") {
            return { _error: '`Surname` is required.' }
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
                name: 'organisation',
                label: 'Organisation',
                field: 'Select',
                lazy: () => organisationOptions.read(crudl.req()).then(res => ({
                    helpText: 'Select an account',
                    ...res
                })),
            },
            {
                name: 'title',
                label: 'Title',
                field: 'String',
            },
            {
                name: 'givenName',
                label: 'Given Name',
                field: 'String',
            },
            {
                name: 'familyName',
                label: 'Family Name',
                field: 'String',
            },
            {
                name: 'status',
                label: 'Status',
                field: 'Select',
                options: personStatuses
            },
            {
                name: 'mobile',
                label: 'Mobile',
                field: 'String',
            },
            {
                name: 'email',
                label: 'Email',
                field: 'String',
            },
            {
                name: 'dateOfBirth',
                label: 'Date of birth',
                field: 'Date',
            },
            {
                name: 'dobIsEstimate',
                label: 'DoB Is Estimate',
                field: 'Checkbox',
                helpText: 'Is the date of birth an exact date or estimate?'
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
    path: 'people/new',
    title: 'New Person',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return people.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
