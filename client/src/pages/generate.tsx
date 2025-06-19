import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { useGenerateVideoMutation } from "@/hooks/use-generate-video"
import { Sparkles, Video } from "lucide-react"
import { useState } from "react"

export default function GeneratePage() {
  const generateVideo = useGenerateVideoMutation()
  const [text, setText] = useState("")

  const handleGenerate = () => {
    generateVideo.mutate(text)
  }
  return (
    <div className="w-full h-screen flex justify-center items-center">
      <Card className="w-[40rem]">
        <CardHeader>
          <CardTitle>Buat Video</CardTitle>
          <CardDescription>
            Tulis skrip videomu di bawah, dan biarkan AI menghidupkannya{" "}
            <Sparkles
              className="inline animate-pulse text-violet-700"
              size={16}
            />
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            rows={10}
            className="h-40 resize-none"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Pedesaan adalah tempat yang identik dengan suasana tenang..."
          />
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button disabled={text.length === 0} onClick={handleGenerate}>
            <Video />
            Buat Video
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
