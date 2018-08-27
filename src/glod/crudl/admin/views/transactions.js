import { optionsFromMap, select } from '../utils'
import React from 'react'

import { transactions } from '../connectors/transactions'
import { subjectOptions } from '../connectors/subjects'
import { fundOptions } from "../connectors/funds"


const paymentMethodMap = {
    BankCharges: 'BankCharges',
    BankTax: 'BankTax',
    BillpayOnline: 'BillpayOnline',
    CashLodgmentEnvelopes: 'CashLodgmentEnvelopes',
    CashLodgmentOther: 'CashLodgmentOther',
    CashLodgmentPlate: 'CashLodgmentPlate',
    Cheque: 'Cheque',
    DirectDebit: 'DirectDebit',
    DirectPayment: 'DirectPayment',
    DirectTransfer: 'DirectTransfer',
    InBranch: 'InBranch',
    StandingOrderMonthly: 'StandingOrderMonthly',
    StandingOrderOther: 'StandingOrderOther',
    StandingOrderQuarterly: 'StandingOrderQuarterly',
    StandingOrders: 'StandingOrders',
    UnrealisedGainLoss: 'UnrealisedGainLoss',
}
let paymentMethods = optionsFromMap(paymentMethodMap)

const incomeExpenditureMap = {
    Income: 'Income',
    Expenditure: 'Expenditure'
}
let incomeExpenditures = optionsFromMap(incomeExpenditureMap)

//-------------------------------------------------------------------
const listView = {
    path: 'transactions',
    title: 'Transactions',
    actions: {
        list: function (req) { return transactions.read(req) }
    },
}

// id, referenceNo, publicCode, year, month, day, paymentMethod, description, amount, subject, incomeExpenditure, FY, fund
listView.fields = [
    {
        name: 'referenceNo',
        label: 'Ref. No.',
        sortable: true,
        sorted: 'descending',
        sortpriority: '4',
        main: true
    },
    {
        name: 'publicCode',
        label: 'Public code',
        sortable: true
    },
    {
        name: 'year',
        label: 'Year',
        sortable: true,
        sorted: 'descending',
        sortpriority: '1'
    },
    {
        name: 'month',
        label: 'Month',
        sortable: true,
        sorted: 'descending',
        sortpriority: '2'
    },
    {
        name: 'day',
        label: 'Day',
        sortable: true,
        sorted: 'descending',
        sortpriority: '3'
    },
    {
        name: 'paymentMethod',
        label: 'Payment method',
        render: value => paymentMethodMap[value],
        sortable: true,
    },
    {
        name: 'description',
        label: 'Description',
        sortable: true,
    },
    {
        name: 'amount',
        label: 'Amount',
        render: 'number',
        sortable: true
    },
    {
        name: 'subject',
        label: 'Subject',
        getValue: select('subject.name'),
        sortable: true,
    },
    {
        name: 'incomeExpenditure',
        label: 'Income/Expenditure',
        render: value => incomeExpenditureMap[value],
        sortable: true
    },
    {
        name: 'FY',
        label: 'FY',
        render: 'number',
        sortable: true
    },
    {
        name: 'fund',
        label: 'Fund',
        getValue: select('fund.name'),
        sortable: true
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
            name: 'publicCode',
            label: 'Public code',
            field: 'Search',
        },
        {
            name: 'year',
            label: 'Year',
            field: 'Search',
        },
        {
            name: 'month',
            label: 'Month',
            field: 'Search',
        },
        {
            name: 'day',
            label: 'Day',
            field: 'Search',
        },
        {
            name: 'paymentMethod',
            label: 'Payment method',
            field: 'Select',
            options: paymentMethods
        },
        {
            name: 'description',
            label: 'Description',
            field: 'Search',
        },
        {
            name: 'amount',
            label: 'Amount',
            field: 'Search',
        },
        {
            name: 'subject',
            label: 'Subject',
            field: 'Select',
            lazy: () => subjectOptions.read(crudl.req()).then(res => ({
                helpText: 'Select a subject',
                ...res
            })),
        },
        {
            name: 'incomeExpenditure',
            label: 'Income/Expenditure',
            field: 'Select',
            options: incomeExpenditures
        },
        {
            name: 'FY',
            label: 'FY',
            render: 'number',
            field: 'Search',
        },
        {
            name: 'fund',
            label: 'Fund',
            field: 'Select',
            lazy: () => fundOptions.read(crudl.req()).then(res => ({
                helpText: 'Select a fund',
                ...res
            })),
        }

    ]
}

//-------------------------------------------------------------------
const changeView = {
    path: 'transactions/:id',
    title: 'Transaction',
    tabtitle: 'Main',
    actions: {
        get: req => transactions(crudl.path.id).read(req),
        delete: req => transactions(crudl.path.id).delete(req),
        save: req => transactions(crudl.path.id).update(req),
    },
    validate: function (values) {
        if (!values.referenceNo || values.referenceNo == "") {
            return { _error: '`Reference number` is required.' }
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
            },
            {
                name: 'publicCode',
                label: 'Public code',
                field: 'String',
            },
            {
                name: 'year',
                label: 'Year',
                field: 'String',
            },
            {
                name: 'month',
                label: 'Month',
                field: 'String',
            },
            {
                name: 'day',
                label: 'Day',
                field: 'String',
            },
            {
                name: 'paymentMethod',
                label: 'Payment method',
                field: 'Select',
                options: paymentMethods
            },
            {
                name: 'description',
                label: 'Description',
                field: 'String',
            },
            {
                name: 'amount',
                label: 'Amount',
                field: 'String',
            },
            {
                name: 'subject',
                label: 'Subject',
                getValue: select('subject.id'),
                field: 'Select',
                lazy: () => subjectOptions.read(crudl.req()).then(res => ({
                    helpText: 'Select a subject',
                    ...res
                })),
            },
            {
                name: 'incomeExpenditure',
                label: 'Income/Expenditure',
                field: 'Select',
                options: incomeExpenditures
            },
            {
                name: 'FY',
                label: 'FY',
                render: 'number',
                field: 'String',
            },
            {
                name: 'fund',
                label: 'Fund',
                getValue: select('fund.id'),
                field: 'Select',
                lazy: () => fundOptions.read(crudl.req()).then(res => ({
                    helpText: 'Select a subject',
                    ...res
                })),
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
const addView = {
    path: 'transactions/new',
    title: 'New Transaction',
    fieldsets: changeView.fieldsets,
    validate: changeView.validate,
    actions: {
        add: function (req) { return transactions.create(req) },
    },
}

//-------------------------------------------------------------------
module.exports = {
    listView,
    addView,
    changeView,
}
