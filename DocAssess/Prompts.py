question_prompt = """
You are a helpful assistant that finds weaknesses in Bank's AI model documents. Please analyze the following document and point out weaknesses only as per the category and points mentioned below.
Give around 3-4 brief points of 'Weaknesses' with 'Suggestions for improvement'.
{question}
For this task, please adhere to the following guidelines:
Ensure clear and direct communication of ideas without ambiguity.
Use the fewest words possible while maintaining clarity and completeness.
Choose precise language to accurately convey ideas without unnecessary elaboration.
Focus only on information directly related to the topic or purpose, avoiding tangents.
Structure the text logically with clear transitions between ideas and sections.

Document: {context}

Weaknesses:
"""

style_template = """Category: Style. Points for Evaulation:
1. Make sure The document has version control and stakeholders' details.
2. A given section or sub-section should have the relevant narrative and be complete.
3. For all the listed assumptions and limitations, ensure proper justification is provided.
4. Ensure that the document has a page number.
5. Ensure all validation/development tests have a conclusion.
"""

context_template = """Category: Context. Points for Evaulation:
1. An effective development process begins with a clear statement of purpose to ensure that model 
development is aligned with the intended use. The design, theory, and logic underlying the model 
should be well-documented and generally supported by published research and sound industry 
practice. 
2. The model methodologies and processing components that implement the theory, 
including the mathematical specification and the numerical techniques and approximations, should 
be explained in detail with particular attention to merits and limitations. 
3. Reports should be clear and comprehensible and take into account the fact that decision makers and 
modelers often come from quite different backgrounds and may interpret the contents in different 
ways. Make sure any report is not missing or inadequately explained in the document
"""

quality_template = """Category: Quality, Points for Evaulation:
Verify that model document includes information supporting decisions related to 
model selection, testing, governance, development, internal controls, and third-party risk
management. Consider whether documentation includes 
• model assumptions and limitations in consideration of the model's use. 
• theoretical approach and supporting research, as appropriate. 
• model design and formulas. 
• data coverage, sources, quality, and limitations. 
• description and interpretation of testing diagnostics, model outcomes, and expected 
performance under a variety of economic conditions and business environments. 
• an explanation of the degree to which underlying input-output relationships predict 
model outcomes. 
• change logs. 
• ongoing monitoring plans. 
• a description, frequency, and standards of monitoring for each model, including 
performance metrics used in ongoing monitoring, performance thresholds, and 
supporting rationale. 
• business uses.
If not please point out the section.
"""

examination_template = """
Provide suggestions to improve the document that helps in the reduction of the risk of an examination, particularly you identiify changes in:
• policies, procedures, or processes. 
• personnel. 
• control systems. 
• use of data. 
• models. 
• model performance. 
• information systems. 
• third-party relationships. 
• products or services. 
• delivery channels or volumes. 
• markets. 
• economic environment. 
• geographies.
"""

question_template = [style_template, context_template, quality_template, examination_template]
category_list = ["Style", "Context", "Quality", "Examination"]
