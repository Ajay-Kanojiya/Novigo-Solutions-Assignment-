from enum import Enum
from io import BytesIO
from typing import Optional
from fillpdf import fillpdfs
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, Form, HTTPException


app = FastAPI(
    title="Novigo Solutions Assignment 🚀",
    summary="A FastAPI API that accepts form data, fills out the fields in a provided PDF form, and returns a PDF.",
    description=
    '''
    Requirements:

        - Use the provided sample_pdf.pdf form.
        - Fill the form with the supplied data.
        - Return the filled PDF as a response.
    ''',
    version="v1.0.0",
)


class Activity(str, Enum):
    reading = "Reading"
    walking = "Walking"
    music = "Music"
    other = "Other"


@app.post("/fillpdf",  tags=["fillPdfEndpoint"])
async def fill_pdf(
    pdf_file: UploadFile = File(...),
    name: str = Form(...),
    address: str = Form(...),
    favorite_activities: str = Form(..., title="Favorite Activities Tick Boxs", description="Comma-separated list of favorite activities"),
    other_activity_Mtbox: Optional[str] = Form("", description="Specify other activity if 'Other' is selected"),
    favorite_activity: int = Form(..., title="Favorite Activity Radio Buttons", description="Radio Buttons (only one option can be selected : 0 - Reading, 1 - Walking, 2 - Music, 3 - Other", ge=0, le=3),
    other_activity_Rbtn: Optional[str] = Form("", description="Specify other activity if 'Other' is selected"),
):
    '''
    ### Enter a comma-separated list of favorite activities: 
            Reading, Walking, Music, Other
    '''
    try:
        # Parse the favorite activities into a list of Activity enums
        favorite_activities_list = [Activity(act.strip()) for act in favorite_activities.split(",")]

        # Read the uploaded PDF file content
        pdf_content = await pdf_file.read()
        pdf_stream = BytesIO(pdf_content)

        # Map form inputs to PDF field names
        field_mapping = {
            'Name': name,
            'Address': address,
            'Check Box1': 'Yes' if Activity.reading in favorite_activities_list else 'Off',
            'Check Box2': 'Yes' if Activity.walking in favorite_activities_list else 'Off',
            'Check Box3': 'Yes' if Activity.music in favorite_activities_list else 'Off',
            'Check Box4': 'Yes' if Activity.other in favorite_activities_list else 'Off',
            'Group6': str(favorite_activity),  # Replace with the actual field name
            'Text5': other_activity_Mtbox if Activity.other in favorite_activities_list else '',
            'Text6': other_activity_Rbtn if Activity.other in favorite_activities_list else ''
        }

        # Fill the PDF form using fillpdf and BytesIO
        filled_pdf_stream = BytesIO()
        fillpdfs.write_fillable_pdf(pdf_stream, filled_pdf_stream, field_mapping)
        filled_pdf_stream.seek(0)


        return StreamingResponse(filled_pdf_stream, media_type='application/pdf', headers={
            'Content-Disposition': 'attachment; filename="filled_form.pdf"'
        })

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8060)
