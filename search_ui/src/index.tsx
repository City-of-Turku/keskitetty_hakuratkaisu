import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'overmind-react'
import { createGlobalStyle } from 'styled-components'
import { App, AppAttribute } from './App'
import { overmind } from './AppState'
import { getConfiguration } from './BackendAPI'

const GlobalStyle = createGlobalStyle`
  .keha-ui-application,
  .keha-ui-application input, button {
    font-family: 'Roboto', sans-serif;
    font-weight: 300;
    /* font-size: 16px; */
    color: rgba(0, 0, 0, .8);
  }
`

export const getProp = (attrs: AppAttribute[], name: string): null | string => {
  for (const attr of attrs) {
    if (attr.name === name) return attr.value
  }
  return null
}

const renderApp = async (renderElement: Element, bundleElement: Element | null) => {
  const attrs: AppAttribute[] = []
  const names = renderElement.getAttributeNames().filter(name => name.indexOf('data-') === 0)
  for (const name of names) {
    const value = renderElement.getAttribute(name) || ''
    const ap: AppAttribute = { name, value }
    attrs.push(ap)
  }
  if (bundleElement) {
    const names = bundleElement.getAttributeNames().filter(name => name.indexOf('data-') === 0)
    for (const name of names) {
      const value = bundleElement.getAttribute(name) || ''
      const ap: AppAttribute = { name, value }
      attrs.push(ap)
    }
  }

  const backendRoot = getProp(attrs, 'data-backend-root') || 'http://localhost:5000'
  const config = await getConfiguration(backendRoot)
  console.log('configuration from backend', config)

  ReactDOM.render(
    <React.StrictMode>
      <Provider value={overmind}>
        <GlobalStyle />
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;700&display=swap" rel="stylesheet" />
        <App attrs={attrs} config={config} />
      </Provider>
    </React.StrictMode>,
    renderElement
  )
}

const jsElement = document.getElementById('keskitetty-hakuratkaisu-bundle')
const elements = document.getElementsByClassName('keskitetty-hakuratkaisu') || []
for (let i = 0; i < elements.length; i++) {
  renderApp(elements[i], jsElement)
}
