# Creative AI Studio

**Comprehensive Generative AI Platform for Business Content Creation and Editing**

## Project Description

Creative AI Studio is a web application developed as part of the AI Master's program at the European Graduate Institute. The platform integrates multiple generative artificial intelligence models to create a complete solution aimed at marketing, design, and content creation teams.

The project addresses the business need to generate high-quality visual and textual content efficiently, incorporating collaborative workflows and ethical AI usage policies.

## Project Objectives

### Main Objective
Develop a platform that allows different user roles (designers, writers, approvers) to collaborate in content creation using state-of-the-art generative AI.

### Specific Objectives
- Implement image generation with granular control of styles and parameters
- Provide intelligent text editing tools for multiple purposes
- Establish a role and permission system for different types of users
- Create collaborative workflows with project management
- Incorporate security measures and ethical AI usage
- Demonstrate practical integration of AWS services for AI

## Technical Architecture

### Technologies Used

**Frontend and Interface**
- **Streamlit**: Main framework for web interface
- **Python**: Base programming language
- **PIL (Pillow)**: Image processing
- **JSON**: Structured data handling

**Backend and AI**
- **Amazon Bedrock**: AI as a service platform
- **Stable Diffusion XL**: Image generation model
- **Claude v2 (Anthropic)**: Natural language processing model
- **boto3**: AWS SDK for Python

**Infrastructure and Deploy**
- **AWS**: Cloud services for AI
- **Streamlit Cloud**: Deployment platform
- **GitHub**: Version control and CI/CD

### System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   AWS Bedrock   │
│   (Streamlit)   │◄──►│   (Python +      │◄──►│                 │
│                 │    │    boto3)        │    │ • Stable Diff.  │
│ • UI Components │    │                  │    │ • Claude v2     │
│ • Session State │    │ • Authentication │    │ • Model APIs    │
│ • Role Mgmt     │    │ • API Calls      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Main Features

### 1. Intelligent Image Generation

**Features:**
- Text-to-image conversion using Stable Diffusion XL
- 18 predefined styles (anime, photographic, digital art, etc.)
- Configurable parameters:
  - Prompt precision (cfg_scale): 1-20
  - Generation steps: 10-100
  - Dimensions: 512x512, 768x768, 1024x1024
- Deterministic or random generation via seed control

**Workflow:**
1. User enters textual description
2. Selects desired artistic style
3. Adjusts advanced parameters (optional)
4. System sends request to Amazon Bedrock
5. Stable Diffusion processes and generates image
6. Image is displayed and stored in personal gallery

**Result Management:**
- Complete history of generated images
- Metadata: original prompt, style, timestamp, user
- Download system in PNG format
- Gallery filterable by style and user
- Preview in 3-column grid

### 2. Text Content Editing

**System Capabilities:**
- **Text improvement**: Optimization of clarity and professionalism
- **Intelligent summarization**: Condensation maintaining key points
- **Content expansion**: Addition of relevant details and examples
- **Grammar correction**: Error detection and correction
- **Creative rewriting**: Stylistic content transformation

**Editing Process:**
1. User enters original text
2. Selects desired operation type
3. Claude v2 processes content according to instruction
4. System presents side-by-side comparison (before/after)
5. Result is stored in editing history

**Version Control:**
- Complete history of all edits
- Visual comparison between versions
- Metadata for each operation
- Reversion to previous versions
- Traceability by user and timestamp

### 3. Role and Permission System

**User Architecture:**

**Designer**
- Unlimited image generation
- Access to complete gallery
- Advanced parameter configuration
- No access to text editing

**Writer**
- Textual content editing and improvement
- Full access to editing history
- Correction and rewriting tools
- No access to image generation

**Approver**
- Visualization of all content
- Ability to approve or reject
- Read-only access to creation tools
- Approval workflow management

**Administrator**
- Full access to all functionalities
- User and permission management
- Security policy configuration
- System monitoring and auditing

### 4. Collaboration and Project Management

**Project System:**
- Project creation with description and metadata
- Assignment of content (images/texts) to specific projects
- Progress tracking and statistics
- Contributor management per project

**Collaborative Tools:**
- Real-time team chat
- Comment system per project
- Activity notifications
- Active user list
- Pending task management

**Typical Workflow:**
1. Administrator creates new project
2. Assigns specific roles to team members
3. Designers generate visual assets
4. Writers create and refine textual content
5. Approvers review and validate content
6. Project is marked as complete

### 5. Security and Ethical Use

**Content Policies:**
- Automatic filters for inappropriate content
- Clearly defined ethical usage guidelines
- Respect for copyright and trademarks
- Prevention of harmful or biased content

**Security Measures:**
- Encryption of stored data
- Complete activity auditing
- Granular access control
- AWS credential protection
- Logging of all operations

**Administrative Settings:**
- Per-user limits (images/day)
- Text length restrictions
- Default parameter configuration
- Retention policy management

## Business Use Cases

### Digital Marketing Agency
**Scenario**: Multi-platform advertising campaign creation
- Designers generate visual variations for different channels
- Writers adapt copy for different audiences
- Approvers validate brand consistency
- Smooth collaboration between remote teams

### Corporate Content Department
**Scenario**: Educational materials production
- Generation of explanatory illustrations
- Adaptation of technical texts for different levels
- Versioning and change control
- Approval by technical experts

### E-commerce Startup
**Scenario**: Catalog content creation
- Massive product image generation
- SEO description optimization
- A/B testing of variations
- Scalability without additional hiring

## System Data Flow

```
1. User Authentication → 2. Role Selection → 3. Access to Features

4a. Image Generation:
   Input Text → Bedrock API → Stable Diffusion → Base64 → PIL → Display

4b. Text Editing:
   Input Text → Prompt Engineering → Claude API → Response → Comparison View

5. Storage in Session State → 6. Persistence in History

7. Project Management → 8. Collaboration → 9. Approval
```

## Technical Considerations

### Implemented Optimizations
- **Caching**: Use of `@st.cache_resource` for Bedrock client
- **Session State**: Data persistence during session
- **Lazy Loading**: On-demand component loading
- **Error Handling**: Robust API error handling
- **Responsive Design**: Adaptation to different screen sizes

### Known Limitations
- Dependency on AWS connectivity
- Variable costs according to model usage
- Bedrock rate limiting constraints
- Temporary storage (non-persistent)
- Specific region required (us-east-1)

### Future Scalability
- Integration with persistent databases
- Implementation of distributed cache
- Load balancing for multiple users
- Integration with storage services (S3)
- REST API for external integrations

## Metrics and Evaluation

### System KPIs
- Average image generation time: ~10-15 seconds
- Text editing accuracy: Qualitative evaluation by users
- User satisfaction: Measurement through post-use surveys
- System availability: >99% uptime target

### Test Cases
1. **Image Generation**: "A red cat jumping" → Verify visual coherence
2. **Text Editing**: Technical paragraph improvement → Evaluate clarity
3. **Collaboration**: Complete designer → writer → approver flow
4. **Security**: Inappropriate content generation attempt → Effective blocking

## Installation and Configuration

### System Requirements
- Python 3.9 or higher
- AWS account with Bedrock access
- IAM credentials with specific permissions
- Stable internet connection

### Minimum AWS Configuration
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### Required Environment Variables
```
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_DEFAULT_REGION=us-east-1
```

## Project Conclusions

Creative AI Studio demonstrates the technical and commercial viability of integrating multiple generative AI services into a coherent business platform. The project successfully addresses the challenges of:

- **Technological integration** between different AI models
- **User experience** intuitive for non-technical users
- **Business collaboration** with granular roles and permissions
- **Ethical use** through implemented policies and controls
- **Technical scalability** using cloud architecture

The solution provides a solid foundation for developing generative AI business applications, combining technical power with ease of use and ethical considerations necessary for responsible business adoption.

## Academic Project Information

**Institution**: European Graduate Institute  
**Program**: Master's in Artificial Intelligence  
**Subject**: Generative AI  
**Unit**: 3 - Practical Applications of Generative AI  
**Focus**: Complete business solution development

**Academic Objectives Achieved**:
- Practical implementation of generative AI models
- Integration of cloud services for AI (AWS Bedrock)
- Development of user interfaces for AI
- Ethical considerations in AI systems
- Technology project management
- Deployment and operation of AI applications
