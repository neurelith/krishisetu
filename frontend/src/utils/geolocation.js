export function hasValidCoordinatePair(latitude, longitude) {
  if (latitude === null || latitude === '' || longitude === null || longitude === '') return false
  const lat = Number(latitude)
  const lon = Number(longitude)
  return Number.isFinite(lat) && lat >= -90 && lat <= 90 &&
    Number.isFinite(lon) && lon >= -180 && lon <= 180
}

export function requestDeviceCoordinates(geolocation) {
  if (!geolocation) {
    return Promise.reject({ code: 0, message: 'Geolocation is not supported.' })
  }

  return new Promise((resolve, reject) => {
    geolocation.getCurrentPosition(
      ({ coords }) => {
        resolve({
          latitude: roundCoordinate(coords.latitude),
          longitude: roundCoordinate(coords.longitude)
        })
      },
      reject,
      { enableHighAccuracy: false, timeout: 12000, maximumAge: 300000 }
    )
  })
}

export function getLocationErrorState(error) {
  return error?.code === 1 ? 'denied' : 'unavailable'
}

function roundCoordinate(value) {
  return Math.round((Number(value) + Number.EPSILON) * 100000) / 100000
}
