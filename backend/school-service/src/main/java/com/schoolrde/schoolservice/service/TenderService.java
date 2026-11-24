package com.schoolrde.schoolservice.service;
//DTO-to-Entity and Entity-to-DTO mapping is implemented with AI assistance

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.TenderDao;
import com.schoolrde.schoolservice.dao.repository.TenderStatusRepository;
import com.schoolrde.schoolservice.dto.DocumentResponseDto;
import com.schoolrde.schoolservice.dto.TenderRequestDto;
import com.schoolrde.schoolservice.dto.TenderResponseDto;
import com.schoolrde.schoolservice.entity.TenderEntity;
import com.schoolrde.schoolservice.entity.TenderStatus;
import com.schoolrde.schoolservice.exception.CustomException;


@Service
public class TenderService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(TenderService.class);
	
	public static final Integer CATEGORY_TENDER = 5;

	private final TenderDao tenderDao;
    private final DocumentService documentService;
    private final TenderStatusRepository tenderStatusRepository;


	public TenderService(TenderDao tenderDao, DocumentService documentService, TenderStatusRepository tenderStatusRepository){
	    this.tenderDao = tenderDao;
	    this.documentService = documentService;
	    this.tenderStatusRepository = tenderStatusRepository;
	}

	
	public List<TenderResponseDto> getTenderByProjectId(Integer projectId){

	    LOGGER.info("Fetching tenders for projectId: {}", projectId);

	    List<TenderEntity> tenderEntities = tenderDao.findTenderByProjectId(projectId);

	    if(tenderEntities.isEmpty()){
	        LOGGER.warn("Tenders not found for projectId: {}", projectId);
	        throw new CustomException("E9007");
	    }

	    List<TenderResponseDto> tenderResponseDtos = new ArrayList<>();

	    for(TenderEntity tenderEntity : tenderEntities){
	        tenderResponseDtos.add(convertToTenderResponseDto(tenderEntity));
	    }

	    return tenderResponseDtos;
	}

	public TenderResponseDto getTenderById(Integer id){

	    LOGGER.info("Fetching tender with id: {}", id);

	    TenderEntity tenderEntity = tenderDao.findTenderById(id)
	                    .orElseThrow(()->{
	                        LOGGER.warn("Tender not found with id: {}", id);
	                        return new CustomException("E9007");
	                    });

	    return convertToTenderResponseDto(tenderEntity);
	}

	public Integer createTender(TenderRequestDto tenderRequestDto){

	    LOGGER.info("Creating tender");
	    
	    if(tenderDao.existsByTenderNumber(tenderRequestDto.getTenderNumber())){
	    	LOGGER.warn("Tender already exists with tender number: {}", tenderRequestDto.getTenderNumber());
	    	throw new CustomException("E9008");
	    }
	       
	    TenderEntity tenderEntity = new TenderEntity();
	    tenderEntity.setProjectId(tenderRequestDto.getProjectId());
	    tenderEntity.setTenderNumber(tenderRequestDto.getTenderNumber());
	    tenderEntity.setTenderTitle(tenderRequestDto.getTenderTitle());
	    tenderEntity.setTenderDescription(tenderRequestDto.getTenderDescription());
	    TenderStatus tenderStatus = tenderStatusRepository.findByStatus(tenderRequestDto.getTenderStatus())
                .orElseGet(()->{
                    LOGGER.warn("Tender status not found with status {}, setting tender status to OTHER", tenderRequestDto.getTenderStatus());
                    return tenderStatusRepository.findByStatus("OTHER")
                            .orElseThrow(()-> new CustomException("E9007"));
                });
	    tenderEntity.setTenderStatus(tenderStatus);
	    tenderEntity.setEstimatedAmount(tenderRequestDto.getEstimatedAmount());
	    tenderEntity.setAwardedAmount(tenderRequestDto.getAwardedAmount());
	    tenderEntity.setPublicationDate(tenderRequestDto.getPublicationDate());
	    tenderEntity.setSubmissionDeadline(tenderRequestDto.getSubmissionDeadline());
	    tenderEntity.setAwardDate(tenderRequestDto.getAwardDate());
	    tenderEntity.setContractorName(tenderRequestDto.getContractorName());
	    tenderEntity.setContractStartDate(tenderRequestDto.getContractStartDate());
	    tenderEntity.setContractEndDate(tenderRequestDto.getContractEndDate());

	    TenderEntity savedEntity = tenderDao.saveTender(tenderEntity);

	    LOGGER.info("Tender created successfully with id: {}", savedEntity.getId());

	    return savedEntity.getId();
	}

	private TenderResponseDto convertToTenderResponseDto(TenderEntity tenderEntity){

	    LOGGER.info("Converting TenderEntity to TenderResponseDto");

	    TenderResponseDto tenderResponseDto = new TenderResponseDto();

	    tenderResponseDto.setId(tenderEntity.getId());
	    tenderResponseDto.setProjectId(tenderEntity.getProjectId());
	    tenderResponseDto.setTenderNumber(tenderEntity.getTenderNumber());
	    tenderResponseDto.setTenderTitle(tenderEntity.getTenderTitle());
	    tenderResponseDto.setTenderDescription(tenderEntity.getTenderDescription());
        tenderResponseDto.setTenderStatus(tenderEntity.getTenderStatus().getStatus());
	    tenderResponseDto.setEstimatedAmount(tenderEntity.getEstimatedAmount());
	    tenderResponseDto.setAwardedAmount(tenderEntity.getAwardedAmount());
	    tenderResponseDto.setPublicationDate(tenderEntity.getPublicationDate());
	    tenderResponseDto.setSubmissionDeadline(tenderEntity.getSubmissionDeadline());
	    tenderResponseDto.setAwardDate(tenderEntity.getAwardDate());
	    tenderResponseDto.setContractorName(tenderEntity.getContractorName());
	    tenderResponseDto.setContractStartDate(tenderEntity.getContractStartDate());
	    tenderResponseDto.setContractEndDate(tenderEntity.getContractEndDate());
	    List<DocumentResponseDto> tenderDocuments = documentService
	    		.getDocumentByObjectIdAndObjectCategoryId(tenderEntity.getId(), CATEGORY_TENDER);
	    tenderResponseDto.setTenderDocuments(tenderDocuments);

	    return tenderResponseDto;
	}
}
