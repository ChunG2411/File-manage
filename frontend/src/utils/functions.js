
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
