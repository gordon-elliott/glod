import { continuousPagination, listQuery, transformErrors } from '../utils'

module.exports = {

    // Accounts
    accounts: {
        query: {
            read: listQuery({
                name: 'accounts',
                fields: 'id, referenceNo, purpose, status, name, institution, sortCode, accountNo, BIC, IBAN',
                args: { first: 7 }
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
    },
    account:{
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
                    throw crudl.notFoundError('The requested account was not found')
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
    },

    // AUTHENTICATION
    login: {
        url: '/rest-api/login/',
        mapping: { read: 'post', },
        transform: {
            readResponse: res => {
                if (res.status >= 400) {
                    const error = res.data
                    if (error !== null && typeof error === 'object') {
                        error._error = error.non_field_errors
                    }
                    throw new crudl.ValidationError(error)
                }
                return res
            },
            readResponseData: data => ({
                requestHeaders: { "Authorization": `Token ${data.token}` },
                info: data,
            })
        }
    }
}
