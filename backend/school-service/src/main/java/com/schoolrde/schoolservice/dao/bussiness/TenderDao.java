package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.TenderEntity;

public interface TenderDao{
	
    TenderEntity saveTender(TenderEntity tender);

    List<TenderEntity> findTenderByProjectId(Integer projectId);

    Optional<TenderEntity> findTenderById(Integer id);
    
    boolean existsByTenderNumber(String tenderNumber);


}
