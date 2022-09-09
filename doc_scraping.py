import re
from urllib import response
from lxml import html

# This function grabs the case details for each individual column from the document for a given case.
# Returns a dictionary containing the case details

def get_details(row,tree,court_complex = "Rohini Court Complex",region = "North",district = "Delhi"):

    Id = "" 

    CombinedCaseNumber = row['case_info'].replace('/','-')
    
    CaseNumber = row['case_info'].split('/')[1]

    CaseType = row['case_info'].split('/')[0]

    Year = row['case_info'].split('/')[2]   

    CourtName = tree.xpath('//h1/span/text()')[0]

    try:
        CourtHallNumber = tree.xpath("//div[@align='center']/div[2]/span[5]/label/strong[2]/text()")[0].split('-')[0]
        CourtHallNumber = ''.join(filter(str.isalnum, CourtHallNumber))
    except:
        CourtHallNumber = ""

    Bench = "" 

    try:    
        DateFiled = tree.xpath("//div[@align = 'center']/div/span[3]/span[2]/text()")[0].split(':')[1].strip()
    except:
        DateFiled = ""

    CaseClassification = ""
    OrderType = ""


    Petitioner = row['parties'][0]

    try:
        PetitionerAdvocate = ""
        for ele in tree.xpath("//div[@align = 'center']/div[3]/span[1]//text()"):
            if(ele.lower().find("advocate") != -1):
                PetitionerAdvocate = ele[ele.lower().find("advocate")+10:]
                break
    except:
        PetitionerAdvocate = ""

    Respondent = row['parties'][1]
    
    try:
        RespondentAdvocate = ""
        for ele in tree.xpath("//div[@align = 'center']/div[3]/span[2]//text()"):
            if(ele.lower().find("advocate") != -1):
                RespondentAdvocate = ele[ele.lower().find("advocate")+10:]
                break
    except:
        RespondentAdvocate = ""


# To Improve
    try:
        CurrentStage = tree.xpath("//div[@align = 'center']/div[2]/span[3]/label/strong[2]/text()")[0].split(':')[1].strip()
    except:
        CurrentStage = ""

# To Improve
    try:
        CurrentStatus = tree.xpath("//div[@align = 'center']/div[2]/span[3]/label/strong[2]/text()")[0].split(':')[1].strip()
    except:
        CurrentStatus = ""
    
    District = region

    LastActionTaken = ""

    LatestOrder = ""

    try:
        BeforeHonarbleJudges = tree.xpath("//div[@align='center']/div[2]/span[5]/label/strong[2]/text()")[0].split('-')[1].strip()
    except:
        BeforeHonarbleJudges = ""

    LastPostedFor = ""
    
    LastDateOfAction = ""

    NextHearingDate = "" 
    LowerCourtName = ""

    LowerCourtCaseNumber = ""

    LowerCourtOtherDetails = ""

    LowerCourtDisposalDate = ""

    CaseGroup = ""

    LastSyncTime = ""

    RespondentType = "RESPONDENT"
    
    PetitionerType = "PETITIONER"

    PresentedOn = ""

    BenchCategory = ""

    CaseOriginatedFrom = ""

    ListedTimes = ""

    Act = ""

    DisposalDate = ""

    LastListedOn = ""

    CaseCategory = ""

    CurrentPosition = ""

    NextListingPurpose = ""

    Purpose = tree.xpath("//div[@align='center']/table[@align='center'][1]/tbody/tr/td[5]/text()")[-1].strip()

    try:
        FilingNumber = re.split(':|/', tree.xpath("//div[@align='center']/div[1]/span[3]/text()")[0] )[1]
    except:
        FilingNumber = ""

    SerialNumber = row['srno']

    try:
        cnr_number = tree.xpath("//div[@align='center']/div/b/span/text()")[0].split(':')[1]
    except:
        cnr_number = ""

    CaseUpdateOn = ""
    
    PoliceStationName = ""

    NextListingCourt = ""

    try:
        RegistrationDate = tree.xpath("//div[@align='center']/div/span[4]/span[2]/label[2]/text()")[0].split(':')[1]
    except:
        RegistrationDate = ""

    ActionDate = ""

    NextListingDate = ""

    StageName = CurrentStage

    PostingStage = ""

    ListingDate = ""

    NextListingTime = ""

    DepartmentName = ""

    LowerCourtJudgmentDate = ""

    PresentDate = ""

    StampNumber = ""

    DateOfHearing = ""

    LowerCourtDistrict = ""

    LowerCourtJudges = ""

    Subject = ""

    CauseListDate = ""

    RegistrationNo = row['case_info'].split('/')[1]
        
    try:
        DecisionDate = tree.xpath(" //div[@align='center']/div[2]/span[2]//strong[2]/text()")[0].split(":")[1]
    except:
        DecisionDate = ""

    try:
        NatureOfDisposal = tree.xpath("//div[@align='center']/div[2]/span[4]//strong[2]/text()")[0].split(":")[1]
    except:
        NatureOfDisposal = ""

    PetitionerAddress = ""

    RespondentAddress = ""

    try:
        UnderActs = tree.xpath("//div[@align='center']/div[3]/table//tr[2]/td[1]/text()")[0].strip()
    except:
        UnderActs = ""

    try:
        UnderSections = tree.xpath("//div[@align='center']/div[3]/table//tr[2]/td[2]/text()")[0].strip()
    except:
        UnderSections = ""

    try:
        PoliceStation = tree.xpath("//div[@align='center']/div[4]/span/label[1]/span/text()")[0].strip()
    except:
        PoliceStation = ""

    try:
        FIRNo = tree.xpath("//div[@align='center']/div[4]/span/label[2]/text()")[0].split(':')[1].strip()
    except:
        FIRNo = ""

    BusinessOnDate = ""

    hearing_business = ""

    CourtState = "Delhi"

    CourtType = "Court Establishment"

    CourtDistrict = "Central"

# To Improve
    StageOfCase = "" 

    CourtComplex = court_complex

    try:
        FirstHearingDate = tree.xpath("//div[@align='center']/div[2]/span[1]/label/strong[2]/text()")[0].split(":")[1].strip()
    except:
        FirstHearingDate = ""

    try:
        ParsingYear = re.split(':|/', tree.xpath("//div[@align='center']/div[1]/span[3]/text()")[0] )[2]
    except:
        ParsingYear = ""

    try:
        Njdg_Judge_Name = tree.xpath("//div[@align='center']/div[2]/span[5]/label/strong[2]/text()")[0].split('-')[1].strip()
    except:
        Njdg_Judge_Name = ""

    try:
        Full_Identifier = district + "--" + region + "--" + CourtName+"--"+RegistrationNo+"--"+SerialNumber
    except:
        Full_Identifier = ""

    try:
        CaseUniqueValue = district + "--" + region + "--" + CourtName+"--"+SerialNumber+"--"+court_complex+'-'+CombinedCaseNumber+'-'+'CNR Number:'+cnr_number+'-'+CurrentStatus.split(' ')[1]
    except:
        CaseUniqueValue = ""
    
    try:
        NoOfHearings = len ( tree.xpath("//div[@align='center']/table[@align='center'][1]//tr[position() >= 2]") )
    except:
        NoOfHearings = 0

    try:
        NoOfOrders = len( tree.xpath("//div[@align='center']/table[@align='center']") ) - 2 
    except:
        NoOfOrders = 0

    try:
        JudgementPDFlink = "https://services.ecourts.gov.in/ecourtindia_v4_bilingual/cases/" + tree.xpath("//div[@align='center']//table/tbody/tr/td[3]/a/@href")[-1]
    except:
        JudgementPDFlink = ""

    JudgementContent = ""
        
    details = {
        "Id" : Id,
        "CombinedCaseNumber" : CombinedCaseNumber,
        "CaseNumber" : CaseNumber,
        "CaseType" : CaseType,
        "Year" : Year,
        "CourtName" : CourtName,
        "CourtHallNumber" : CourtHallNumber,
        "Bench" : Bench,
        "DateFiled" : DateFiled,
        "CaseClassification" : CaseClassification,
        "OrderType" : OrderType,
        "Petitioner" : Petitioner,
        "PetitionerAdvocate" : PetitionerAdvocate,
        "Respondent" : Respondent,
        "RespondentAdvocate" : RespondentAdvocate,
        "CurrentStage" : CurrentStage,
        "CurrentStatus" : CurrentStatus,
        "District" : District,
        "LastActionTaken" : LastActionTaken,
        "LatestOrder" : LatestOrder,
        "BeforeHonarbleJudges" : BeforeHonarbleJudges,
        "LastPostedFor" : LastPostedFor,
        "LastDateOfAction" : LastDateOfAction,
        "NextHearingDate" : NextHearingDate,
        "LowerCourtName" : LowerCourtName,
        "LowerCourtCaseNumber" : LowerCourtCaseNumber,
        "LowerCourtOtherDetails" : LowerCourtOtherDetails,
        "LowerCourtDisposalDate" : LowerCourtDisposalDate,
        "CaseGroup" : CaseGroup,
        "LastSyncTime" : LastSyncTime,
        "RespondentType" : RespondentType,
        "PetitionerType" : PetitionerType,
        "PresentedOn" : PresentedOn,
        "BenchCategory" : BenchCategory,
        "CaseOriginatedFrom" : CaseOriginatedFrom,
        "ListedTimes" : ListedTimes,
        "Act" : Act,
        "DisposalDate" : DisposalDate, 
        "LastListedOn" : LastListedOn,
        "CaseCategory" : CaseCategory,
        "CurrentPosition" : CurrentPosition,
        "NextListingPurpose" : NextListingPurpose,
        "Purpose" : Purpose,
        "FilingNumber" : FilingNumber,
        "SerialNumber" : SerialNumber,
        "cnr_number" : cnr_number,
        "CaseUpdateOn" : CaseUpdateOn,
        "PoliceStationName" : PoliceStationName,
        "NextListingCourt" : NextListingCourt,
        "RegistrationDate" : RegistrationDate,
        "ActionDate" : ActionDate,
        "NextListingDate" : NextListingDate,
        "StageName" : StageName,
        "PostingStage" : PostingStage,
        "ListingDate" : ListingDate,
        "NextListingTime" : NextListingTime,
        "DepartmentName" : DepartmentName,
        "LowerCourtJudgmentDate" : LowerCourtJudgmentDate,
        "PresentDate" : PresentDate,
        "StampNumber" : StampNumber,
        "DateOfHearing" : DateOfHearing,
        "LowerCourtDistrict" : LowerCourtDistrict,
        "LowerCourtJudges" : LowerCourtJudges,
        "Subject" : Subject,
        "CauseListDate" : CauseListDate,
        "RegistrationNo" : RegistrationNo,
        "DecisionDate" : DecisionDate,
        "NatureOfDisposal" : NatureOfDisposal,
        "PetitionerAddress" : PetitionerAddress,
        "RespondentAddress" : RespondentAddress,
        "UnderActs" : UnderActs,
        "UnderSections" : UnderSections,
        "PoliceStation" : PoliceStation,
        "FIRNo" : FIRNo,
        "BusinessOnDate" : BusinessOnDate, 
        "hearing_business" : hearing_business,
        "CourtState" : CourtState,
        "CourtType" : CourtType,
        "CourtDistrict" : CourtDistrict,
        "StageOfCase" : StageOfCase,
        "CourtComplex" : CourtComplex,
        "FirstHearingDate" : FirstHearingDate,
        "ParsingYear" : ParsingYear,
        "Njdg_Judge_Name" : Njdg_Judge_Name,
        "Full_Identifier" : Full_Identifier,
        "CaseUniqueValue" : CaseUniqueValue,
        "NoOfHearings" : NoOfHearings,
        "NoOfOrders" : NoOfOrders,
        "JudgementPDFlink" : JudgementPDFlink,
        "JudgementContent" : JudgementContent
    }

    return details