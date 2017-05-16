import React from 'react'

//-------------------------------------------------------------------
var listView = {
    path: 'subjects',
    title: 'Subjects',
    actions: {
        list: function (req) {
            let subjects = crudl.connectors.subjects.read(req)
            return subjects
        }
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
var changeView = {
    path: 'subjects/:id',
    title: 'Subject',
    tabtitle: 'Main',
    actions: {
        get: function (req) { return crudl.connectors.subject(crudl.path.id).read(req) },
        save: function (req) { return crudl.connectors.subject(crudl.path.id).update(req) },
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
var addView = {
    path: 'subjects/new',
    title: 'New Subject',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return crudl.connectors.subjects.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
