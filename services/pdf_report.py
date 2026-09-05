from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf_report(report, filename="careerpilot_interview_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    content = []

    content.append(
        Paragraph(
            "CareerPilot AI - Interview Report",
            title_style
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Overall Score: {report['overall_score']}/100",
            heading_style
        )
    )

    content.append(
        Paragraph(
            f"Technical Knowledge: "
            f"{report['technical_knowledge']}/100",
            normal_style
        )
    )

    content.append(
        Paragraph(
            f"Problem Solving: "
            f"{report['problem_solving']}/100",
            normal_style
        )
    )

    content.append(
        Paragraph(
            f"Communication: "
            f"{report['communication']}/100",
            normal_style
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph("Strengths", heading_style)
    )

    strengths = [
        ListItem(
            Paragraph(str(item), normal_style)
        )
        for item in report["strengths"]
    ]

    content.append(
        ListFlowable(
            strengths,
            bulletType="bullet"
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Areas to Improve",
            heading_style
        )
    )

    weaknesses = [
        ListItem(
            Paragraph(str(item), normal_style)
        )
        for item in report["weaknesses"]
    ]

    content.append(
        ListFlowable(
            weaknesses,
            bulletType="bullet"
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Recommended Topics",
            heading_style
        )
    )

    topics = [
        ListItem(
            Paragraph(str(item), normal_style)
        )
        for item in report["topics_to_improve"]
    ]

    content.append(
        ListFlowable(
            topics,
            bulletType="bullet"
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Final Recommendation",
            heading_style
        )
    )

    content.append(
        Paragraph(
            str(report["final_recommendation"]),
            normal_style
        )
    )

    doc.build(content)

    return filename