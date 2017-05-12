import { continuousPagination, listQuery, transformErrors } from '../utils'

var nominalAccounts = {
    query: {
        read: listQuery({
            name: 'nominalAccounts',
            fields: 'id, code, description, SOFAHeading, category, subCategory',
            args: { first: 60 },
            prepareFilters: object => {
                let args = Object.getOwnPropertyNames(object).map(name => {
                    if (['SOFAHeading', 'category', 'subCategory'].includes(name)) {
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
            nominalAccountCreate(input: $input) {
                errors
                nominalAccount {id, code, description, SOFAHeading, category, subCategory}
            }
        }`,
    },
    pagination: continuousPagination,
    transform: {
        readResponseData: data => data.data.nominalAccounts.edges.map(e => e.node),
        createResponseData: data => {
            if (data.data.nominalAccountCreate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.nominalAccountCreate.errors))
            }
            return data.data.nominalAccountCreate.nominalAccount
        },
    },
}

var nominalAccount = {
    query: {
        read: `{nominalAccount(id: "%id"){id, code, description, SOFAHeading, category, subCategory}}`,
        update: `mutation ($input: AccountUpdateLeafInput!) {
            nominalAccountUpdate(input: $input) {
                errors
                nominalAccount {id, code, description, SOFAHeading, category, subCategory}
            }
        }`,
    },
    transform: {
        readResponseData: data => {
            if (!data.data.nominalAccount) {
                throw new crudl.NotFoundError('The requested nominal account was not found')
            }
            return data.data.nominalAccount
        },
        updateResponseData: data => {
            if (data.data.nominalAccountUpdate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.nominalAccountUpdate.errors))
            }
            return data.data.nominalAccountUpdate.nominalAccount
        },
    }
}

module.exports = {
    nominalAccounts,
    nominalAccount
}
