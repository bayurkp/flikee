export interface GenerateVideoResponse {
  message: string
  execution_time: number
  result: {
    voiceover: {
      name: string
      url: string
    }
    subtitle: {
      name: string
      url: string
    }
    video: {
      name: string
      url: string
      clips: {
        name: string
        url: string
      }[]
    }
  }
  keywords: string[]
  relevant_videos: {
    source: string
    keyword: string
    description: string
    url: string
    duration: number
    width: number
    height: number
    thumbnail: string
    similarity_score: number
  }
}
