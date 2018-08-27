import { accounts, accountsOptions } from './accounts'
import { funds, fundOptions } from './funds'
import { nominalAccounts, nominalAccountOptions } from './nominalAccounts'
import { parishioners, parishionerOptions } from './parishioners'
import { organisations, organisationOptions } from './organisations'
import { people, personOptions } from './people'
import { addresses, addressOptions } from './addresses'
import { subjects, subjectOptions } from './subjects'
import { statementItems, statementItemOptions } from './statementItems'
import { transactions, transactionOptions } from './transactions'

module.exports = {

    accounts: accounts,
    accountsOptions: accountsOptions,

    funds: funds,
    fundOptions: fundOptions,

    nominalAccounts: nominalAccounts,
    nominalAccountOptions: nominalAccountOptions,

    parishioners: parishioners,
    parishionerOptions: parishionerOptions,

    organisations: organisations,
    organisationOptions: organisationOptions,

    people: people,
    personOptions: personOptions,

    addresses: addresses,
    addressOptions: addressOptions,

    subjects: subjects,
    subjectOptions: subjectOptions,

    statementItems: statementItems,
    statementItemOptions: statementItemOptions,

    transactions: transactions,
    transactionOptions: transactionOptions,

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
