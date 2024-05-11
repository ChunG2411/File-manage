import vi from '../assets/lang/vi.json' assert {type: 'json'}
import en from '../assets/lang/en.json' assert {type: 'json'}
import zh from '../assets/lang/zh.json' assert {type: 'json'}


export function formatDate(datetime) {
    const date = datetime.split('T')[0]
    const time = datetime.split('T')[1].split('.')[0]
    return date + ' ' + time
}

export function differentDate(datetime) {
    const now = new Date()
    const givenDatetime = new Date(datetime)
    const timeDifference = givenDatetime.getTime() - now.getTime()
    return Math.floor(Math.abs(timeDifference) / 1000 / 60 / 60 / 24)
}

export function formatSize(size) {
    const int_size = parseFloat(size)
    const mb_unit = 1024
    const gb_unit = 1024 * 1024
    if (int_size > gb_unit) {
        return `${(int_size/gb_unit).toFixed(2)} Gb`
    }
    else if (int_size < gb_unit && int_size > mb_unit) {
        return `${(int_size/mb_unit).toFixed(2)} Mb`
    }
    else return `${int_size} Kb`
}

export function getText(lang, file, pos) {
    if (lang=='zh') {
        return zh[file][pos]
    }
    else if (lang=='en') {
        return en[file][pos]
    }
    else {
        return vi[file][pos]
    }
}
