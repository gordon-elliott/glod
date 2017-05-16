import { continuousPagination, listQuery, transformErrors } from '../utils'

var statementItems = {
    query: {
        read: listQuery({
            name: 'statementItems',
            fields: 'id, account{id, name, IBAN}, date, details, currency, debit, credit, balance',
            args: { first: 20 },
            prepareFilters: object => {
                let args = Object.getOwnPropertyNames(object).map(name => {
                    if (['account', 'date', 'debit', 'credit', 'balance'].includes(name)) {
                        return `${name}: ${object[name]}`
                    }
                    else {
                        return `${name}: "${object[name]}"`
                    }
                }).join(', ')
                return args ? `{${args}}` : ''
            }
        }),
        create: `mutation ($input: StatementItemCreateLeafInput!) {
            statementItemCreate(input: $input) {
                errors
                statementItem {id, account{id, name, IBAN}, date, details, currency, debit, credit, balance}
            }
        }`,
    },
    pagination: continuousPagination,
    transform: {
        readResponseData: data => data.data.statementItems.edges.map(e => e.node),
        createResponseData: data => {
            if (data.data.statementItemCreate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.statementItemCreate.errors))
            }
            return data.data.statementItemCreate.statementItem
        },
    },
}

var statementItem = {
    query: {
        read: `{statementItem(id: "%id"){id, account{id, name, IBAN}, date, details, currency, debit, credit, balance}}`,
        update: `mutation ($input: StatementItemUpdateLeafInput!) {
            statementItemUpdate(input: $input) {
                errors
                statementItem {id, account{id, name, IBAN}, date, details, currency, debit, credit, balance}
            }
        }`,
    },
    transform: {
        readResponseData: data => {
            if (!data.data.statementItem) {
                throw new crudl.NotFoundError('The requested statement item was not found')
            }
            return data.data.statementItem
        },
        updateResponseData: data => {
            if (data.data.statementItemUpdate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.statementItemUpdate.errors))
            }
            return data.data.statementItemUpdate.statementItem
        },
    }
}

module.exports = {
    statementItems,
    statementItem
}
