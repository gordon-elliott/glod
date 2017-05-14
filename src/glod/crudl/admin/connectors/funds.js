import { continuousPagination, listQuery, transformErrors } from '../utils'

var funds = {
    query: {
        read: listQuery({
            name: 'funds',
            fields: 'id, name, type, isParishFund, account{id, name, IBAN}',
            args: { first: 20 },
            prepareFilters: object => {
                let args = Object.getOwnPropertyNames(object).map(name => {
                    if (['type', 'isParishFund', 'account'].includes(name)) {
                        return `${name}: ${object[name]}`
                    }
                    else {
                        return `${name}: "${object[name]}"`
                    }
                }).join(', ')
                return args ? `{${args}}` : ''
            }
        }),
        create: `mutation ($input: FundCreateLeafInput!) {
            fundCreate(input: $input) {
                errors
                fund {id, name, type, isParishFund, account{id, name, IBAN}}
            }
        }`,
    },
    pagination: continuousPagination,
    transform: {
        readResponseData: data => data.data.funds.edges.map(e => e.node),
        createResponseData: data => {
            if (data.data.fundCreate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.fundCreate.errors))
            }
            return data.data.fundCreate.fund
        },
    },
}

var fund = {
    query: {
        read: `{fund(id: "%id"){id, name, type, isParishFund, account{id, name, IBAN}}}`,
        update: `mutation ($input: FundUpdateLeafInput!) {
            fundUpdate(input: $input) {
                errors
                fund {id, name, type, isParishFund, account{id, name, IBAN}}
            }
        }`,
    },
    transform: {
        readResponseData: data => {
            if (!data.data.fund) {
                throw new crudl.NotFoundError('The requested fund was not found')
            }
            return data.data.fund
        },
        updateResponseData: data => {
            if (data.data.fundUpdate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.fundUpdate.errors))
            }
            return data.data.fundUpdate.fund
        },
    }
}

module.exports = {
    funds,
    fund
}
