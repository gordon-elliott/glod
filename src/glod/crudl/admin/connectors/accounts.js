import { continuousPagination, listQuery, transformErrors } from '../utils'

var accounts = {
    query: {
        read: listQuery({
            name: 'accounts',
            fields: 'id, referenceNo, purpose, status, name, institution, sortCode, accountNo, BIC, IBAN',
            args: { first: 7 },
            prepareFilters: object => {
                let args = Object.getOwnPropertyNames(object).map(name => {
                    if (['referenceNo', 'status'].includes(name)) {
                        return `${name}: ${object[name]}`
                    }
                    else {
                        return `${name}: "${object[name]}"`
                    }
                }).join(', ')
                return args ? `{${args}}` : ''
            }
        }),
        create: `mutation ($input: AccountCreateLeafInput!) {
            accountCreate(input: $input) {
                errors
                account {id, referenceNo, purpose, status, name, institution, sortCode, accountNo, BIC, IBAN}
            }
        }`,
    },
    pagination: continuousPagination,
    transform: {
        readResponseData: data => data.data.accounts.edges.map(e => e.node),
        createResponseData: data => {
            if (data.data.accountCreate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.accountCreate.errors))
            }
            return data.data.accountCreate.account
        },
    },
}

var account = {
    query: {
        read: `{account(id: "%id"){id, referenceNo, purpose, status, name, institution, sortCode, accountNo, BIC, IBAN}}`,
        update: `mutation ($input: AccountUpdateLeafInput!) {
            accountUpdate(input: $input) {
                errors
                account {id, referenceNo, purpose, status, name, institution, sortCode, accountNo, BIC, IBAN}
            }
        }`,
    },
    transform: {
        readResponseData: data => {
            if (!data.data.account) {
                throw new crudl.NotFoundError('The requested account was not found')
            }
            return data.data.account
        },
        updateResponseData: data => {
            if (data.data.accountUpdate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.accountUpdate.errors))
            }
            return data.data.accountUpdate.account
        },
    }
}

module.exports = {
    accounts,
    account
}
