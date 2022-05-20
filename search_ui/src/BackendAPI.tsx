import axios, { AxiosRequestConfig, Method } from 'axios'
import { Configuration } from './Interfaces'

export const executeRequest = async (backendRoot: string, method: Method, url: string, data: any) => {
  const headers = {
    'X-Requested-With': 'XMLHttpRequest',
  }
  const options: AxiosRequestConfig = {
    baseURL: backendRoot,
    url,
    method,
    headers,
    data,
    timeout: 1000 * 30,
    responseType: 'json',
  }
  console.debug('axios request options', options)
  try {
    const res = await axios.request(options)
    console.debug('axios response for %s %s', method, url, res)
    return res
  } catch (error) {
    console.error('axios error for %s %s', method, url, error)
    throw error
  }
}

export const getConfiguration = async (backendRoot: string): Promise<Configuration> => {
  try {
    const res = await executeRequest(backendRoot, 'GET', '/config', null)
    if (res.status !== 200) {
      throw new Error('response status ' + res.status)
    }
    return res.data
  } catch(error) {
    return {
      analytics: {},
      content_types: [],
      languages: [],
    }
  }
}
