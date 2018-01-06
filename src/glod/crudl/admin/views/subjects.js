import React from 'react'

import { subjects } from '../connectors/subjects'
import {funds} from "../connectors/funds";

//-------------------------------------------------------------------
const listView = {
    path: 'subjects',
    title: 'Subjects',
    actions: {
        list: function (req) { return subjects.read(req) }
    },
}

// id, name, selectVestrySummary, easterVestrySummary
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
        name: 'selectVestrySummary',
        label: 'Select Vestry Summary',
        sortable: true,
    },
    {
        name: 'easterVestrySummary',
        label: 'Easter Vestry Summary',
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
            name: 'selectVestrySummary',
            label: 'Select Vestry Summary',
            field: 'Search',
        },
        {
            name: 'easterVestrySummary',
            label: 'Easter Vestry Summary',
            field: 'Search',
        },
    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'subjects/:id',
    title: 'Subject',
    tabtitle: 'Main',
    actions: {
        get: req => subjects(crudl.path.id).read(req),
        delete: req => subjects.delete(req), // the request contains the id already
        save: req => subjects.update(req), // the request contains the id already
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
                name: 'selectVestrySummary',
                label: 'Select Vestry Summary',
                field: 'String',
            },
            {
                name: 'easterVestrySummary',
                label: 'Easter Vestry Summary',
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
    path: 'subjects/new',
    title: 'New Subject',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return subjects.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
