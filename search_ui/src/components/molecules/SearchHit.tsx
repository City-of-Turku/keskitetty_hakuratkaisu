import { ReactNode, useState } from 'react'
import styled from 'styled-components'
import { SearchResult, ContentType } from '../../Interfaces'
import { LinkIcon, MapMarkerIcon, PhoneIcon, CalendarIcon } from '../../assets/Icons'
import { formatDate } from '../../Utils'
import { useAppState } from '../../AppState'

const Hit = styled.div.attrs({role: 'listitem', className: 'kehauicss-result-hit'})`
  margin: 0 0 32px;
  padding: 0 0 32px;
`

const TagBoxFont = styled.div`
  color: rgba(0, 0, 0, .8);
  font-size: 0.875em;
  font-weight: 300;
`

const TagBox = styled(TagBoxFont).attrs({className: 'kehauicss-result-tagbox'})`
  background-color:rgba(0, 0, 0, 0.1);
  border-radius: 2px;
  display: inline-block;
  padding: 5px 8px;
  margin: 0 .5em .5em 0;
`

const ContentTypeBoxElement = styled(TagBox)<{ accentColor: string}>`
  border: 1px solid ${p => p.accentColor};
  background-color: transparent;
  color: ${p => p.accentColor};
  padding: 5px 12px;
`
const ContentTypeBox = ({children}: {children: ReactNode}) => {
  const { accentColor } = useAppState()
  return <ContentTypeBoxElement accentColor={accentColor}>{children}</ContentTypeBoxElement>
}

const Title = styled.h2.attrs({className: 'kehauicss-result-title'})`
  margin: 0 0 12px;
  font-size: 1.75em;
  font-weight: 700;
  text-decoration: underline;
`

const Snippet = styled.div.attrs({className: 'kehauicss-result-snippet'})`
  margin: 0 0 12px;

  em {
    font-weight: 500;
    font-style: normal;
  }
`

const UrlElement = styled.div.attrs({className: 'kehauicss-result-url'})`
  margin: 0 0 16px;
  display: flex;
  align-items: center;

  font-size: 0.875em;
  font-weight: 300;
  color: rgba(0, 0, 0, .7);
  text-decoration: none;
  word-break: break-all;
  span {
    font-weight: 400;
    color: rgba(0, 0, 0, .8);
  }

  em {
    display: none; // hidden, change if score debugging is needed
    font-size: 0.75em;
    font-style: normal;
    font-weight: 300;
    color: #ccc;
    margin-left: 1em;
  }
  svg {
    margin-right: 4px;
    color: #000;
    min-width: 14px;
  }
`
const Url = ({children}: {children: ReactNode}) => {
  return <UrlElement>{children}</UrlElement>
}

const Tags = styled.div`
  margin: 1em 0 0;
`

const MoreTags = styled(TagBoxFont)`
  display: inline-block;
  cursor: pointer;
`

const InfoIcons = styled.div.attrs({className: 'kehauicss-result-infoicons'})`
  margin: .5em 0;
  display: flex;
  align-items: center;
  font-weight: 300;

  svg {
    height: 20px;
    margin-right: 4px;
  }
  span {
    margin-right: 12px;
  }
`

const HitAuthor = styled.div.attrs({className: 'kehauicss-result-author'})`
  display: inline-block;
  font-size: 0.875em;
  margin: 0 6px;
`

const HitDate = styled.div.attrs({className: 'kehauicss-result-date'})`
  display: inline-block;
  font-size: 0.875em;
  margin: 0 6px;
`

const ContactGrid = styled.div<{ hasImage: boolean }>`
  display: grid;
  grid-template-columns: ${p => p.hasImage ? '200px auto' : '1fr'};
  gap: 24px;
  margin-top: 12px;
`

const ContactPhoto = styled.div.attrs({className: 'kehauicss-result-contact-photo'})`
  width: 200px;
  height: 200px;
  background-position: center;
  background-size: cover;
`

const EventPhoto = styled.div.attrs({className: 'kehauicss-result-event-photo'})`
  width: 640px;
  height: 360px;
  max-width: 100%;
  background-position: center;
  background-size: cover;
`

const RenderTags = ({ tags }: { tags: string[] }) => {
  const limit = 4;
  const [showMoreLink, setShowMoreLink] = useState(tags.length > limit)
  if (tags.length === 0) return null;
  const subset = showMoreLink ? tags.slice(0, limit) : tags
  const numberOfMore = tags.length - limit
  return (
    <Tags>
      {subset.map(tag => <TagBox key={tag}>{tag}</TagBox>)}
      {showMoreLink && <MoreTags onClick={() => setShowMoreLink(false)}>{numberOfMore} lisää &gt;</MoreTags>}
    </Tags>
  )
}

const cleanUrl = (url: string) => {
  if (typeof url !== 'string') {
    return {
      domain: 'INVALID.URL',
      path: '/',
    }
  }
  let processed =  url.replace(/^https?:\/\/(www\.)?/, '')
  if (processed.indexOf('/') === -1) processed += '/'
  const firstSlash = processed.indexOf('/')
  const domain = processed.substring(0, firstSlash)
  let path = processed.substring(firstSlash)
  const maxlen = 25
  if (path.length > maxlen) {
    path = path.substring(0, maxlen) + '...'
  }
  return {
    domain,
    path
  }
}

const A = styled.a<{ accentColor: string }>`
  text-decoration: none;
  color: inherit;
  transition: color .5s;
  &:hover, &:focus {
    color: ${p => p.accentColor};
    text-decoration: underline;
  }
`

const typeLabel = (contentType: ContentType) => {
  if (contentType) {
    let label = contentType.replaceAll('_', ' ').toLocaleLowerCase()
    return label.charAt(0).toUpperCase() + label.substring(1)
  }
  return ''
}

const HitGeneric = ({ result }: { result: SearchResult }) => {
  const state = useAppState()
  const {domain, path} = cleanUrl(result.url)
  const date = formatDate(result.date)
  const showInfoIcons = result.place || result.phone
  return (
    <Hit>
      <ContentTypeBox>{typeLabel(result.contentType)}</ContentTypeBox>
      {date && <HitDate>{date}</HitDate>}
      {result.author && <HitAuthor>{result.author}</HitAuthor>}
      <Title><A href={result.url} accentColor={state.accentColor}>
        {result.title}
      </A></Title>
      {showInfoIcons &&
        <InfoIcons>
          {result.place && <><MapMarkerIcon /> <span>{result.place}</span></>}
          {result.phone && <><PhoneIcon /> <span>{result.phone}</span></>}
        </InfoIcons>
      }
      <Snippet dangerouslySetInnerHTML={{ __html: result.snippet }} />
      <Url><LinkIcon /><span>{domain}</span>{path} <em>{result.score.toFixed(1)}</em></Url>
      {result.image && <EventPhoto style={{ backgroundImage: `url(${result.image})` }}></EventPhoto>}
      <RenderTags tags={result.themes} />
    </Hit>
  )
}

const HitContact = ({ result }: { result: SearchResult }) => {
  const state = useAppState()
  const {domain, path} = cleanUrl(result.url)
  const hasImage = !!result.image
  const showInfoIcons = result.place || result.phone
  return (
    <Hit>
      <ContentTypeBox>{typeLabel(result.contentType)}</ContentTypeBox>
      <ContactGrid hasImage={hasImage}>
        {hasImage && <ContactPhoto style={{ backgroundImage: `url(${result.image})` }}></ContactPhoto>}
        <div>
          <Title><A href={result.url} accentColor={state.accentColor}>
            {result.title}
          </A></Title>
          {showInfoIcons &&
            <InfoIcons>
              {result.place && <><MapMarkerIcon /> <span>{result.place}</span></>}
              {result.phone && <><PhoneIcon /> <span>{result.phone}</span></>}
            </InfoIcons>
          }
          <Snippet dangerouslySetInnerHTML={{ __html: result.snippet }} />
          <Url><LinkIcon /><span>{domain}</span>{path} <em>{result.score.toFixed(1)}</em></Url>
          <RenderTags tags={result.themes} />
        </div>
      </ContactGrid>
    </Hit>
  )
}

const HitEvent = ({ result }: { result: SearchResult }) => {
  const state = useAppState()
  const {domain, path} = cleanUrl(result.url)
  const date = formatDate(result.date)
  return (
    <Hit>
      <ContentTypeBox>{typeLabel(result.contentType)}</ContentTypeBox>
      <InfoIcons>
        {date && <><CalendarIcon /> <span>{date}</span></>}
        {result.place && <><MapMarkerIcon /> <span>{result.place}</span></>}
        {result.phone && <><PhoneIcon /> <span>{result.phone}</span></>}
      </InfoIcons>
      <Title><A href={result.url} accentColor={state.accentColor}>
        {result.title}
      </A></Title>
      <Snippet dangerouslySetInnerHTML={{ __html: result.snippet }} />
      <Url><LinkIcon /><span>{domain}</span>{path} <em>{result.score.toFixed(1)}</em></Url>
      {result.image && <EventPhoto style={{ backgroundImage: `url(${result.image})` }}></EventPhoto>}
      <RenderTags tags={result.themes} />
    </Hit>
  )
}

interface SearchHitProps {
  result: SearchResult
}
export const SearchHit = (props: SearchHitProps) => {
  const result = props.result

  switch (result.contentType) {
    case ContentType.Uutinen:
      return <HitGeneric result={result} />
    case ContentType.Blogi:
      return <HitGeneric result={result} />
    case ContentType.Yhteystieto:
      return <HitContact result={result} />
    case ContentType.Toimipaikka:
      return <HitGeneric result={result} />
    case ContentType.Tapahtuma:
      return <HitEvent result={result} />
    case ContentType.Palvelu:
      return <HitGeneric result={result} />
    default:
      return <HitGeneric result={result} />
  }
}