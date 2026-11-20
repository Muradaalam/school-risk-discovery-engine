package com.schoolrde.schoolservice.service;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.schoolrde.schoolservice.dao.bussiness.TenderDao;
import com.schoolrde.schoolservice.dto.TenderRequestDto;
import com.schoolrde.schoolservice.dto.TenderResponseDto;
import com.schoolrde.schoolservice.entity.TenderEntity;
import com.schoolrde.schoolservice.exception.CustomException;


@Service
public class TenderService{
	
	private static final Logger LOGGER = LoggerFactory.getLogger(TenderService.class);

	private final TenderDao tenderDao;

	public TenderService(TenderDao tenderDao){
	    this.tenderDao = tenderDao;
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

	    TenderEntity tenderEntity = new TenderEntity();
	    tenderEntity.setProjectId(tenderRequestDto.getProjectId());
	    tenderEntity.setTenderNumber(tenderRequestDto.getTenderNumber());
	    tenderEntity.setTenderTitle(tenderRequestDto.getTenderTitle());
	    tenderEntity.setTenderDescription(tenderRequestDto.getTenderDescription());
	    tenderEntity.setTenderStatusId(tenderRequestDto.getTenderStatusId());
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

	    TenderResponseDto TenderResponseDto = new TenderResponseDto();

	    TenderResponseDto.setId(tenderEntity.getId());
	    TenderResponseDto.setProjectId(tenderEntity.getProjectId());
	    TenderResponseDto.setTenderNumber(tenderEntity.getTenderNumber());
	    TenderResponseDto.setTenderTitle(tenderEntity.getTenderTitle());
	    TenderResponseDto.setTenderDescription(tenderEntity.getTenderDescription());
	    TenderResponseDto.setEstimatedAmount(tenderEntity.getEstimatedAmount());
	    TenderResponseDto.setAwardedAmount(tenderEntity.getAwardedAmount());
	    TenderResponseDto.setPublicationDate(tenderEntity.getPublicationDate());
	    TenderResponseDto.setSubmissionDeadline(tenderEntity.getSubmissionDeadline());
	    TenderResponseDto.setAwardDate(tenderEntity.getAwardDate());
	    TenderResponseDto.setContractorName(tenderEntity.getContractorName());
	    TenderResponseDto.setContractStartDate(tenderEntity.getContractStartDate());
	    TenderResponseDto.setContractEndDate(tenderEntity.getContractEndDate());

	    return TenderResponseDto;
	}
}
