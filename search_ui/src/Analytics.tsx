import { useCallback, useEffect, useState } from 'react'
import ReactGA from 'react-ga4'
import TagManager from 'react-gtm-module'
import MatomoTracker from '@datapunt/matomo-tracker-js'
import { useAppState } from './AppState'
import { ConfigurationAnalytics } from './Interfaces'

export const useAnalytics = () => {
  const state = useAppState()
  const [initDone, setInitDone] = useState(false)

  const googleAnalyticsId = useCallback(() => {
    return state.analytics?.google_analytics_id
  }, [state.analytics.google_analytics_id])

  const googleTagManagerId = useCallback(() => {
    return state.analytics?.google_tag_manager_id
  }, [state.analytics.google_tag_manager_id])

  const matomoConfig = useCallback(() => {
    return state.analytics?.matomo || {}
  }, [state.analytics.matomo])

  const pageHitToAnalytics = useCallback(() => {
    console.log('pageHitToAnalytics', {
      gaID: googleAnalyticsId(),
      gtmID: googleTagManagerId(),
    })
    if (googleAnalyticsId()) {
      ReactGA.send({ hitType: 'pageview', page: '/' })
    }
    if (matomoConfig().base_url) {
      const tracker = window.matomoTracker as MatomoTracker
      tracker.trackPageView()
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps
  
  const initAnalytics = useCallback((analytics: ConfigurationAnalytics) => {
    console.log('initAnalytics', analytics)
    const gaId = googleAnalyticsId()
    const gtmId = googleTagManagerId()
    const ma = matomoConfig()
    if (gaId) {
      console.log('initAnalytics: Google Analytics detected', { gaId })
      ReactGA.initialize(gaId)
    }
    if (gtmId) {
      console.log('initAnalytics: Google Tag Manager detected', { gtmId })
      TagManager.initialize({ gtmId })
    }
    if (ma.base_url) {
      console.log('initAnalytics: Matomo detected', ma)
      const tracker = new MatomoTracker({
        urlBase: ma.base_url,
        siteId: ma.site_id || 1,
      })
      console.log('matomo tracker', tracker)
      window.matomoTracker = tracker
    }
    pageHitToAnalytics()
  }, [pageHitToAnalytics, googleAnalyticsId, googleTagManagerId, matomoConfig])

  useEffect(() => {
    if (!initDone) {
      initAnalytics(state.analytics)
      setInitDone(true)
    }
  }, [state.analytics, initAnalytics, initDone])

  const searchHitToAnalytics = (keywords?: string) => {
    keywords = keywords || ''
    const gaId = googleAnalyticsId()
    const gtmId = googleTagManagerId()
    const ma = matomoConfig()
    console.log('searchHitToAnalytics', { gaId, gtmId, ma, keywords })
    if (gaId) {
      ReactGA.send({ hitType: 'pageview', page: '/search?query=' + encodeURIComponent(keywords) })
      ReactGA.event({
        category: 'search',
        action: 'search',
        label: keywords,
      })
    }
    if (gtmId) {
      window.dataLayer = window.dataLayer || []
      window.dataLayer.push({
        event: 'search',
        action: 'search',
        keywords,
      })
    }
    if (ma.base_url && window.matomoTracker) {
      const tracker = window.matomoTracker as MatomoTracker
      tracker.trackPageView({
        href: '/search?query=' + encodeURIComponent(keywords)
      })
      tracker.trackEvent({
        category: 'search',
        action: 'search',
        name: keywords,
      })
    }
  }

  return {
    initAnalytics,
    pageHitToAnalytics,
    searchHitToAnalytics,
  }  
}