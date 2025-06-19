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
import { Download, Loader2, Sparkles, SquarePen, Video } from "lucide-react"
import { useState } from "react"
import { useNavigate } from "react-router"

export default function GeneratePage() {
  const navigate = useNavigate()

  const { mutate, isPending, isSuccess, data, isError, error } =
    useGenerateVideoMutation()
  const [text, setText] = useState("")

  const handleGenerate = () => {
    mutate(text)
  }

  const handleEdit = () => {
    navigate("/edit")
  }

  const handleSave = async () => {
    if (data) {
      try {
        const response = await fetch(data.result.video.url)
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)

        const a = document.createElement("a")
        a.href = url
        a.download = data.result.video.name || "video.mp4"
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
      } catch (err) {
        console.error("Failed to save video:", err)
      }
    }
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
          <div className="w-full aspect-video">
            {isSuccess && !isPending ? (
              <video
                src={data.result.video.url}
                controls
                className="rounded-lg w-full h-full object-contain"
              />
            ) : (
              <Textarea
                className="w-full h-full resize-none"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Pedesaan adalah tempat yang identik dengan suasana tenang..."
              />
            )}
          </div>
        </CardContent>
        <CardFooter className="flex justify-end">
          {isError && <div className="text-destructive">{error.message}</div>}
          {isSuccess && !isPending ? (
            <div className="flex gap-2">
              <Button onClick={handleEdit} variant="outline">
                <SquarePen /> Edit
              </Button>
              <Button onClick={handleSave}>
                <Download /> Simpan
              </Button>
            </div>
          ) : (
            <Button
              disabled={text.length === 0 || isPending}
              onClick={handleGenerate}
            >
              {isPending ? <Loader2 className="animate-spin" /> : <Video />}
              Buat Video
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  )
}
