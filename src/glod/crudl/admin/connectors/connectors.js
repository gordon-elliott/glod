import { accounts, account, accountsOptions } from './accounts'
import { funds, fund } from './funds'
import { nominalAccounts, nominalAccount } from './nominalAccounts'
import { parishioners, parishioner } from './parishioners'
import { subjects, subject } from './subjects'

module.exports = {

    accounts: accounts,
    account: account,
    accountsOptions: accountsOptions,

    funds: funds,
    fund: fund,

    nominalAccounts: nominalAccounts,
    nominalAccount: nominalAccount,

    parishioners: parishioners,
    parishioner: parishioner,

    subjects: subjects,
    subject: subject,

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
