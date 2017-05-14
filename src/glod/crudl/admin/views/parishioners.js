import { formatDate } from '../utils'
import React from 'react'

//-------------------------------------------------------------------
var listView = {
    path: 'parishioners',
    title: 'Parishioners',
    actions: {
        list: function (req) {
            let parishioners = crudl.connectors.parishioners.read(req)
            return parishioners
        }
    },
}

// id, referenceNo, surname, firstName, title, spouse, address1, address2, address3, county, eircode, child1, dob1, child2, dob2, child3, dob3, child4, dob4, telephone, giving, email
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
        name: 'surname',
        label: 'Surname',
        sortable: true,
    },
    {
        name: 'firstName',
        label: 'First Name',
        sortable: true,
    },
    {
        name: 'title',
        label: 'Title',
        sortable: true,
    },
    {
        name: 'spouse',
        label: 'Spouse',
        sortable: true,
    },
    {
        name: 'address1',
        label: 'Address line 1',
        sortable: true,
    },
    {
        name: 'address2',
        label: 'Address line 2',
        sortable: true,
    },
    {
        name: 'address3',
        label: 'Address line 3',
        sortable: true,
    },
    {
        name: 'county',
        label: 'County',
        sortable: true,
    },
    {
        name: 'eircode',
        label: 'Eircode',
        sortable: true,
    },
    {
        name: 'child1',
        label: 'Child 1',
        sortable: true,
    },
    {
        name: 'dob1',
        label: 'Date of birth 1',
        sortable: true,
    },
    {
        name: 'child2',
        label: 'Child 2',
        sortable: true,
    },
    {
        name: 'dob2',
        label: 'Date of birth 2',
        sortable: true,
    },
    {
        name: 'child3',
        label: 'Child 3',
        sortable: true,
    },
    {
        name: 'dob3',
        label: 'Date of birth 3',
        sortable: true,
    },
    {
        name: 'child4',
        label: 'Child 4',
        sortable: true,
    },
    {
        name: 'dob4',
        label: 'Date of birth 4',
        sortable: true,
    },
    {
        name: 'telephone',
        label: 'Telephone',
        sortable: true,
    },
    {
        name: 'giving',
        label: 'Giving',
        sortable: true,
    },
    {
        name: 'email',
        label: 'Email',
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
        // TODO make search case insensitive (at db end?)
        {
            name: 'surname',
            label: 'Surname',
            field: 'Search',
        },
        {
            name: 'firstName',
            label: 'First Name',
            field: 'Search',
        },
        {
            name: 'title',
            label: 'Title',
            field: 'Search',
        },
        {
            name: 'spouse',
            label: 'Spouse',
            field: 'Search',
        },
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
            name: 'eircode',
            label: 'Eircode',
            field: 'Search',
        },
        {
            name: 'child1',
            label: 'Child 1',
            field: 'Search',
        },
        {
            name: 'dob1',
            label: 'Date of birth 1',
            field: 'Search',
        },
        {
            name: 'child2',
            label: 'Child 2',
            field: 'Search',
        },
        {
            name: 'dob2',
            label: 'Date of birth 2',
            field: 'Search',
        },
        {
            name: 'child3',
            label: 'Child 3',
            field: 'Search',
        },
        {
            name: 'dob3',
            label: 'Date of birth 3',
            field: 'Search',
        },
        {
            name: 'child4',
            label: 'Child 4',
            field: 'Search',
        },
        {
            name: 'dob4',
            label: 'Date of birth 4',
            field: 'Search',
        },
        {
            name: 'telephone',
            label: 'Telephone',
            field: 'Search',
        },
        {
            name: 'giving',
            label: 'Giving',
            field: 'Search',
        },
        {
            name: 'email',
            label: 'Email',
            field: 'Search',
        },
    ]
}

//-------------------------------------------------------------------
var changeView = {
    path: 'parishioners/:id',
    title: 'Parishioners',
    tabtitle: 'Main',
    actions: {
        get: function (req) { return crudl.connectors.parishioner(crudl.path.id).read(req) },
        save: function (req) { return crudl.connectors.parishioner(crudl.path.id).update(req) },
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
                name: 'referenceNo',
                label: 'Ref. No',
                field: 'String',
                readOnly: true,
            },
            {
                name: 'surname',
                label: 'Surname',
                field: 'String',
                required: true,
            },
            {
                name: 'firstName',
                label: 'First Name',
                field: 'String',
            },
            {
                name: 'title',
                label: 'Title',
                field: 'String',
            },
            {
                name: 'spouse',
                label: 'Spouse',
                field: 'String',
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
                initialValue: 'Co. Wicklow',
            },
            {
                name: 'eircode',
                label: 'Eircode',
                field: 'String',
            },
            {
                name: 'telephone',
                label: 'Telephone',
                field: 'String',
            },
            {
                name: 'giving',
                label: 'Giving',
                field: 'String',
            },
            {
                name: 'email',
                label: 'Email',
                field: 'String',
            },
        ],
    },
    {
        title: 'Children',
        expanded: false,
        fields: [
            {
                name: 'child1',
                label: 'Child 1',
                field: 'String',
            },
            // TODO get date display and editing working
            {
                name: 'dob1',
                label: 'Date of birth 1',
                field: 'Date',
                props: {
                    formatDate: formatDate
                }
            },
            {
                name: 'child2',
                label: 'Child 2',
                field: 'String',
            },
            {
                name: 'dob2',
                label: 'Date of birth 2',
                field: 'Date',
                props: {
                    formatDate: formatDate
                }
            },
            {
                name: 'child3',
                label: 'Child 3',
                field: 'String',
            },
            {
                name: 'dob3',
                label: 'Date of birth 3',
                field: 'Date',
                props: {
                    formatDate: formatDate
                }
            },
            {
                name: 'child4',
                label: 'Child 4',
                field: 'String',
            },
            {
                name: 'dob4',
                label: 'Date of birth 4',
                field: 'Date',
                props: {
                    formatDate: formatDate
                }
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
var addView = {
    path: 'parishioners/new',
    title: 'New Parishioner',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return crudl.connectors.parishioners.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
