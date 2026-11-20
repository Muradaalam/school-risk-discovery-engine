package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.InspectionEntity;

public interface InspectionDao{
	
    InspectionEntity saveInspection(InspectionEntity inspection);

    List<InspectionEntity> findInspectionBySchoolId(Integer schoolId);

    Optional<InspectionEntity> findInspectionById(Integer id);

}
