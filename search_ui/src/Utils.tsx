import { KeyboardEvent } from 'react'
import { ContentType, SearchResult } from './Interfaces';

export const contentTypeLabel = (id: string) => {
  id = id ? id : ''
  switch (id) {
    case 'tietosivu': return 'Tietosivut'
    case 'uutinen': return 'Uutiset'
    case 'blogi': return 'Blogit'
    case 'yhteystieto': return 'Henkilöt'
    case 'tapahtuma': return 'Tapahtumat'
    case 'palvelu_tai_asiointikanava': return 'Palvelut tai asiointikanavat'
    case 'toimipaikka': return 'Toimipaikat'
    default:
      id = id.replaceAll('_', ' ')
      const label = id.charAt(0).toUpperCase() + id.substring(1)
      console.debug('unknown contentType [%s], using fallback label [%s]', id, label)
      return label
  }
}

export const formatDate = (d?: Date) => {
  if (!d) return null
  const days = ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'];
  return days[d.getDay()] + ' ' + d.getDate() + '.' + (d.getMonth() + 1) + '.' + d.getFullYear()
}

export const detectSiteLanguage = (languages: string[]) => {
  const def = languages[0]
  const htmlLang = document.querySelector('html')?.getAttribute('lang') || ''
  const browserLang = (window.navigator.language || '').split('-')[0]
  console.log('detected language from html [%s] or browser [%s]. supported languages are [%s]', htmlLang, browserLang, languages.join(', '))

  if (languages.indexOf(htmlLang) >= 0) {
    console.log('using html language [%s]', htmlLang)
    return htmlLang
  }
  console.log('html language [%s] is not supported [%s]', htmlLang, languages.join(', '))

  if (languages.indexOf(browserLang) >= 0) {
    console.log('using browser language [%s]', browserLang)
    return browserLang
  }
  console.log('browser language [%s] is not supported [%s]', browserLang, languages.join(', '))

  console.log('using default fallback language [%s]', def)
  return def
}

export const exampleSearchResults: SearchResult[] = [
  {
    url: 'https://example.com/kaikki-metadatat',
    contentType: ContentType.Tietosivu,
    title: 'Kaikki metadatat',
    snippet: 'Lorem ipsum dolor sit amet <em>eleifend</em> nascetur leo tempor <em>cursus</em> consectetuer facilisis facilisi adipiscing vehicula pharetra conubia rhoncus ac habitant quam nullam per enim imperdiet lectus orci dui si duis tempus mollis natoque in torquent malesuada cras netus morbi ultrices aliquet dolor pede litora potenti phasellus euismod vulputate eros feugiat libero tortor nibh proin purus vivamus fusce nisl sed donec nulla magna mattis iaculis porta',
    themes: ['Opetus', 'Varhaiskasvatus'],
    score: 0,
    date: new Date('2022-01-16T18:00:00+03:00'),
    author: 'Kalle Kirjoittaja',
    place: 'Tammitie 3, 20200 Turku',
    phone: '(02) 12345 67890',
    image: 'https://images.unsplash.com/photo-1484684096794-03e03b5e713e?w=600&q=80',
  },
  {
    url: 'https://example.com/tietosivu',
    contentType: ContentType.Tietosivu,
    title: 'Lorem ipsum dolor sit amet',
    snippet: 'Lorem ipsum dolor sit amet <em>eleifend</em> nascetur leo tempor <em>cursus</em> consectetuer facilisis facilisi adipiscing vehicula pharetra conubia rhoncus ac habitant quam nullam per enim imperdiet lectus orci dui si duis tempus mollis natoque in torquent malesuada cras netus morbi ultrices aliquet dolor pede litora potenti phasellus euismod vulputate eros feugiat libero tortor nibh proin purus vivamus fusce nisl sed donec nulla magna mattis iaculis porta',
    themes: ['Opetus', 'Varhaiskasvatus'],
    score: 0,
  },
  {
    url: 'https://example.com/uutinen',
    contentType: ContentType.Uutinen,
    title: 'Suomalainen sauna on kuumin paikka, jonne ihminen menee vapaaehtoisesti',
    snippet: 'Itä-Suomen yliopiston tutkijat ovat huomanneet lukuisia mielenkiintoisia tapoja, joilla sauna vaikuttaa terveyteemme. Uusimman tutkimuksen mukaan ahkera saunominen laskee verenpainetta pitkäkestoisesti.',
    themes: ['Sauna', 'Suomi', 'Kulttuuri'],
    score: 0,
    date: new Date('2021-12-22T12:00:00+03:00'),
    author: 'Matti Virtanen',
  },
  {
    url: 'https://example.com/yhteystieto/john',
    contentType: ContentType.Yhteystieto,
    title: 'James Lipsum',
    snippet: 'Lorem ipsum dolor sit amet quis ullamcorper pede ultrices feugiat laoreet nisl dapibus nec metus purus conubia lacus taciti elit aenean proin platea mus vel dictumst fringilla senectus lorem dignissim libero himenaeos fames posuere aptent aliquam potenti sed porttitor letius malesuada lobortis habitasse natoque odio mi dui sollicitudin placerat fusce eu pulvinar imperdiet curae a torquent egestas tempor penatibus nostra dis massa erat augue molestie',
    themes: ['Tennis', 'Hahmo', 'Omaperäinen'],
    score: 0,
    place: 'Tammitie 3, 20200 Turku',
    phone: '0800 94141',
    image: 'https://images.unsplash.com/photo-1484684096794-03e03b5e713e?w=600&q=80',
  },
  {
    url: 'https://example.com/tapahtuma/karnevaali',
    contentType: ContentType.Tapahtuma,
    title: 'Aurajoen koululaiskarnevaali',
    snippet: 'Lorem ipsum dolor sit amet quis ullamcorper pede ultrices feugiat laoreet nisl dapibus nec metus purus conubia lacus taciti elit aenean proin platea mus vel dictumst fringilla senectus lorem dignissim libero himenaeos fames posuere aptent aliquam potenti sed porttitor letius malesuada lobortis habitasse natoque odio mi dui sollicitudin placerat fusce eu pulvinar imperdiet curae a torquent egestas tempor penatibus nostra dis massa erat augue molestie',
    themes: ['Koulut', 'Ulkotapahtuma', 'Vapaa-aika', 'Lapset ja nuoret', 'Lorem', 'Ipsum', 'Dolor', 'Amet', 'Foobar', 'Something here'],
    score: 0,
    place: 'Turun kauppatori',
    date: new Date('2021-12-22T12:00:00+03:00'),
    image: 'https://images.unsplash.com/photo-1519340241574-2cec6aef0c01?w=600&q=80',
  },
  {
    url: 'https://example.com/toimipaikka/turku',
    contentType: ContentType.Toimipaikka,
    title: 'Turun toimipiste',
    snippet: 'Lorem ipsum dolor sit amet quis ullamcorper pede ultrices feugiat laoreet nisl dapibus nec metus purus conubia lacus taciti elit aenean proin platea mus vel dictumst fringilla senectus lorem dignissim libero himenaeos fames posuere aptent aliquam potenti sed porttitor letius malesuada lobortis habitasse natoque odio mi dui sollicitudin placerat fusce eu pulvinar imperdiet curae a torquent egestas tempor penatibus nostra dis massa erat augue molestie',
    themes: ['toimipiste', 'kunta', 'palvelut'],
    score: 0,
    place: 'Linnankatu 23, 20100 Turku',
    phone: '(02) 12345 67890',
  },
  {
    url: 'https://example.com/blogi',
    contentType: ContentType.Blogi,
    title: 'Trollipeikon Blogi: Koronarokotus',
    snippet: 'Lorem ipsum dolor sit amet quis ullamcorper pede ultrices feugiat laoreet nisl dapibus nec metus purus conubia lacus taciti elit aenean proin platea mus vel dictumst fringilla senectus lorem dignissim libero himenaeos fames posuere aptent aliquam potenti sed porttitor letius malesuada lobortis habitasse natoque odio mi dui sollicitudin placerat fusce eu pulvinar imperdiet curae a torquent egestas tempor penatibus nostra dis massa erat augue molestie',
    themes: ['Korona'],
    score: 0,
    date: new Date('2021-12-09T12:00:00+03:00'),
    author: 'Maija Mallikas',
  },
  {
    url: 'https://example.com/palvelu',
    contentType: ContentType.Palvelu,
    title: 'Kunnallinen palvelupiste',
    snippet: 'Lorem ipsum dolor sit amet quis ullamcorper pede ultrices feugiat laoreet nisl dapibus nec metus purus conubia lacus taciti elit aenean proin platea mus vel dictumst fringilla senectus lorem dignissim libero himenaeos fames posuere aptent aliquam potenti sed porttitor letius malesuada lobortis habitasse natoque odio mi dui sollicitudin placerat fusce eu pulvinar imperdiet curae a torquent egestas tempor penatibus nostra dis massa erat augue molestie',
    themes: ['Palvelu', 'Kunta'],
    score: 0,
    place: 'Tammitie 3, 20200 Turku',
    phone: '(02) 12345 67890',
  },
]

const storageKeySessionKeywords = 'sessionKeywords'
export const storeKeywordsToSession = (keywords?: string) => {
  if (!keywords || keywords.trim().length === 0) return
  let stored = getKeywordsFromSession()
  if (stored.indexOf(keywords) > -1) return
  stored.splice(0, 0, keywords) // add keywords to beginning of the array
  stored = stored.slice(0, 10) // keep max 10 elements
  window.sessionStorage.setItem(storageKeySessionKeywords, JSON.stringify(stored))
}

export const getKeywordsFromSession = (): string[] => {
  const stored = window.sessionStorage.getItem(storageKeySessionKeywords) || '[]'
  try {
    return JSON.parse(stored)
  } catch (e) {
    console.error('getKeywordsFromSession parsing error', e)
    return []
  }
}

export const onKeyEnter = (e: KeyboardEvent<HTMLElement>, callback: () => void) => {
  if (e.code === 'Enter') {
    callback()
    e.preventDefault()
  }
}